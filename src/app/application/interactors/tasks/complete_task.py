from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import TaskNotFoundError, TaskAlreadyDoneError, SessionNotFoundError, \
                                        TaskAccessDeniedError, TaskExecutedTooEarlyError
from src.app.application.dto.tasks import TaskDTO
from src.app.domain import TaskRewardCalculatorDomain
from src.app.domain.enums import TaskRepeatFrequency
from src.app.infrastructure.database.models import TaskHistory, Tasks_history_to_skills
from uuid import UUID
from uuid_utils import uuid7
from datetime import datetime, timezone, timedelta

class CompleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.repo.get_task_with_user_and_skills(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        current_time = datetime.now(timezone.utc)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        if task.repeat_limit is not None:
            if task.repeat_limit == 0:
                raise TaskAlreadyDoneError()
            if task.repeat_limit > 0:
                task.repeat_limit -= 1
        if task.last_completed_at != None:
            match task.repeat_frequency:
                case TaskRepeatFrequency.DAILY:
                    if current_time < task.last_completed_at + timedelta(days=1):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.ONCE_TWO_DAYS:
                    if current_time < task.last_completed_at + timedelta(days=2):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.WEEKLY:
                    if current_time < task.last_completed_at + timedelta(days=7):
                        raise TaskExecutedTooEarlyError()
        task.last_completed_at = current_time
        rewards = TaskRewardCalculatorDomain(
            task_type=task.type, 
            task_difficulty=task.difficulty, 
            task_priority=task.priority, 
            custom_xp_reward=task.custom_xp_reward, 
            custom_gold_reward=task.custom_gold_reward
        ).calculate_task_rewards()

        skills = task.skills
        for skill in skills:
            skill.xp += rewards.xp
            skill.lvl = skill.xp // 1000
        print(task.user.xp)
        task.user.xp = task.user.xp + rewards.xp
        task.user.gold += rewards.gold
        task.user.lvl = task.user.xp // 1000
        
        dto = TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=task.title,
            description=task.description,
            category_id=task.category_id,
            xp=rewards.xp,
            gold=rewards.gold,  
            repeat_limit=task.repeat_limit,
            repeat_frequency=task.repeat_frequency, 
            deadline=task.deadline
        )
        task_history_id = uuid7()
        task_history = TaskHistory(
            id=task_history_id, 
            user_id=task.user_id,
            task_id=task.id, 
            title=task.title, 
            completed_at=current_time, 
            xp_earned=rewards.xp, 
            gold_earned=rewards.gold
        )
        await self.transaction.save(task_history)
        await self.transaction.flush()

        for skill in skills:
            skill_history = Tasks_history_to_skills(
                task_history_id=task_history_id, 
                skill_id=skill.id
            )
            await self.transaction.save(skill_history)

        await self.transaction.commit()
        return dto