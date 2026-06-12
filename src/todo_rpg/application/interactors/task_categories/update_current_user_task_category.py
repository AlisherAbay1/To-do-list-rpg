from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.dto import UpdateTaskCategoryDTO, TaskCategoryDTO
from uuid import UUID
from todo_rpg.application.dto.sentinel_types import Unset
from todo_rpg.application.exceptions import AccessDeniedError, TaskCategoryNotFoundError
from todo_rpg.application.mappers.common import TaskCategoriesMapper


class UpdateCurrentUserTaskCategory:
    def __init__(
        self,
        repo: TaskCategoriesRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, task_category_id: UUID, dto: UpdateTaskCategoryDTO, session_token: str
    ) -> TaskCategoryDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = await self.repo.get_task_category_by_id(task_category_id)
        if task_category is None:
            raise TaskCategoryNotFoundError()
        if task_category.user_id != user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset) and dto.title is not None:
            task_category.title = dto.title
        if not isinstance(dto.color, Unset) and dto.color is not None:
            task_category.color = dto.color

        output_dto = TaskCategoriesMapper.to_dto(task_category)
        await self.uow.commit()
        return output_dto
