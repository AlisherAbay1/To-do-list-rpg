from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import SessionNotFoundError
from src.app.application.dto.tasks import TaskCreateDTO, TaskDTO
from src.app.domain import TaskRewardCalculatorDomain
from src.app.infrastructure.database.models import Task, Tasks_to_skills, Tasks_to_items
from uuid import UUID
from uuid_utils import uuid7

class CreateCurrentUserTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token, dto: TaskCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_id=uuid7()
        task = Task(
            id=task_id,
            user_id=user_id,
            title=dto.title, 
            description=dto.description, 
            category_id=dto.category_id,
            repeat_limit=dto.repeat_limit,
            repeat_frequency=dto.repeat_frequency,
            deadline=dto.deadline,
            type=dto.type, 
            difficulty=dto.difficulty,
            priority=dto.priority,
            custom_xp_reward=dto.custom_xp_reward, 
            custom_gold_reward=dto.custom_gold_reward
        )

        await self.transaction.save(task)
        await self.transaction.flush()

        for skill_id in dto.related_skills:
            relationship = Tasks_to_skills(
                task_id=task_id,
                skill_id=skill_id
            )
            await self.transaction.save(relationship)
        
        for item_id in dto.related_items:
            relationship = Tasks_to_items(
                task_id=task_id,
                item_id=item_id
            )
            await self.transaction.save(relationship)

        await self.transaction.commit()

        rewards = TaskRewardCalculatorDomain(
            task_type=dto.type, 
            task_difficulty=dto.difficulty, 
            task_priority=dto.priority, 
            custom_xp_reward=dto.custom_xp_reward, 
            custom_gold_reward=dto.custom_gold_reward
        ).calculate_task_rewards()

        return TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=dto.title,
            description=dto.description,
            category_id=dto.category_id,
            xp=rewards.xp,
            gold=rewards.gold,  
            repeat_limit=dto.repeat_limit,
            repeat_frequency=dto.repeat_frequency, 
            deadline=dto.deadline
        )