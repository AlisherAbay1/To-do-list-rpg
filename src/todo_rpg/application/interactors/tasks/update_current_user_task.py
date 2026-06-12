from uuid import UUID

from todo_rpg.application.dto import TaskDTO, TaskUpdateDTO
from todo_rpg.application.exceptions import TaskNotFoundError, SessionNotFoundError
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.application.dto.sentinel_types import Unset
from todo_rpg.application.mappers.common import TaskMapper


class UpdateCurrentUserTaskInteractor:
    def __init__(
        self,
        repo: TaskRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(
        self, task_id: UUID, dto: TaskUpdateDTO, session_token: str
    ) -> TaskDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task = await self.repo.get_task_by_id(task_id, user_id)
        if task is None:
            raise TaskNotFoundError()

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

        new_dto = TaskMapper.to_dto(task)
        await self.transaction.commit()
        return new_dto
