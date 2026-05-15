from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
    TaskRepositoryProtocol,
)
from uuid import UUID
from src.app.application.exceptions import (
    TaskCategoryNotFoundError,
    SessionNotFoundError,
    AccessDeniedError,
)
from src.app.application.mappers import ExtendedTaskCategoriesMapper
from src.app.application.dto import TaskCategoryWithTasksDTO


class GetCurrentUserTaskCategoryById:
    def __init__(
        self,
        task_category_repo: TaskCategoriesRepositoryProtocol,
        task_repo: TaskRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.task_category_repo = task_category_repo
        self.task_repo = task_repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, task_category_id: UUID, get_tasks: bool
    ) -> TaskCategoryWithTasksDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = await self.task_category_repo.get_task_category_by_id(
            task_category_id
        )
        if task_category is None:
            raise TaskCategoryNotFoundError()
        if task_category.user_id != user_id:
            raise AccessDeniedError()
        if get_tasks:
            tasks = await self.task_repo.get_tasks_by_category_id(
                task_category_id, user_id
            )
        else:
            tasks = []
        dto = ExtendedTaskCategoriesMapper.to_dto_with_tasks(task_category, tasks)
        return dto
