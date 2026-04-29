from uuid import UUID

from src.app.application.dto.tasks import TaskDTO
from src.app.application.exceptions import (SessionNotFoundError,
                                            AccessDeniedError,
                                            TaskNotFoundError,
                                            UserNotFoundError)
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol, TaskHistoryRepositoryProtocol,
    TaskRepositoryProtocol, UserRepositoryProtocol)
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol
from src.app.application.mappers import TaskMapper

class UncompleteTaskInteractor:
    def __init__(self, 
                 task_repo: TaskRepositoryProtocol, 
                 user_repo: UserRepositoryProtocol, 
                 skill_repo: SkillRepositoryProtocol,
                 task_history_repo: TaskHistoryRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.skill_repo = skill_repo
        self.task_history_repo = task_history_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.task_repo.get_task_by_id(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        tasks_history = await self.task_history_repo.get_recent_history_with_skills(task_id, 2)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if not tasks_history:
            raise TaskNotFoundError()
        if task.user_id != user_id:
            raise AccessDeniedError()
        if task.repeat_limit is not None:
            task.repeat_limit += 1

        before_previous, previous = tasks_history
        user = await self.user_repo.get_user(user_id)
        skills = await self.skill_repo.get_skills_by_task_id(task_id)

        if user is None:
            raise UserNotFoundError()
        
        task.last_completed_at = before_previous.completed_at
        user.xp -= previous.xp_earned
        user.lvl = 1 + user.xp // 1000
        user.gold -= previous.gold_earned
        for skill in previous.skills: 
            skill.xp -= previous.xp_earned

        dto = TaskMapper.to_dto_with_skills_and_user(task, user, skills)
        
        await self.transaction.delete(tasks_history[0])

        await self.transaction.commit()

        return dto