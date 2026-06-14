from todo_rpg.application.interfaces import (
    TaskCategoriesRepositoryProtocol,
    RedisRepositoryProtocol,
    UserRepositoryProtocol,
)
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.mappers.common import TaskCategoriesMapper
from todo_rpg.application.dto import TaskCategoryDTO


class GetAllTaskCategoriesInteractor:
    def __init__(
        self,
        task_categories_repo: TaskCategoriesRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.task_categories_repo = task_categories_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[TaskCategoryDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()
        task_categories = await self.task_categories_repo.get_all_task_categories(
            limit, offset
        )
        return TaskCategoriesMapper.to_list_dto(task_categories)
