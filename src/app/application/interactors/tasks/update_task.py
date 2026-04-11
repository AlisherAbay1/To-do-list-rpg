from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import TaskNotFoundError, TaskAccessDeniedError
from src.app.application.dto.tasks import TaskDTO, TaskUpdateDTO
from src.app.domain import TaskRewardCalculatorDomain
from src.app.presentation.schemas.sentinel_types import Unset
from uuid import UUID

class UpdateTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, dto: TaskUpdateDTO, session_token: str):
        task = await self.repo.get_task_by_id(task_id, False, False)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        
        if not isinstance(dto.title, Unset):
            task.title = dto.title
        if not isinstance(dto.description, Unset):
            task.description = dto.description
        if not isinstance(dto.category_id, Unset):
            task.category_id = dto.category_id
        if not isinstance(dto.repeat_limit, Unset):
            task.repeat_limit = dto.repeat_limit
        if not isinstance(dto.repeat_frequency, Unset):
            task.repeat_frequency = dto.repeat_frequency
        if not isinstance(dto.deadline, Unset):
            task.deadline = dto.deadline
        if not isinstance(dto.type, Unset):
            task.type = dto.type
        if not isinstance(dto.difficulty, Unset):
            task.difficulty = dto.difficulty
        if not isinstance(dto.priority, Unset):
            task.priority = dto.priority
        if not isinstance(dto.custom_xp_reward, Unset):
            task.custom_xp_reward = dto.custom_xp_reward
        if not isinstance(dto.custom_gold_reward, Unset):
            task.custom_gold_reward = dto.custom_gold_reward
        if not isinstance(dto.deleted, Unset):
            task.deleted = dto.deleted

        rewards = TaskRewardCalculatorDomain(
            task_type=task.type, 
            task_difficulty=task.difficulty, 
            task_priority=task.priority, 
            custom_xp_reward=task.custom_xp_reward, 
            custom_gold_reward=task.custom_gold_reward
        ).calculate_task_rewards()
        
        new_dto = TaskDTO(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    category_id=task.category_id,
                    xp=rewards.xp,
                    gold=rewards.gold,
                    repeat_limit=task.repeat_limit,
                    repeat_frequency=task.repeat_frequency,
                    deadline=task.deadline,
                )
        await self.transaction.commit()
        return new_dto