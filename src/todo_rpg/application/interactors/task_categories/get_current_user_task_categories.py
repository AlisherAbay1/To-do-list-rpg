from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.mappers.common import TaskCategoriesMapper
from todo_rpg.application.dto import TaskCategoryDTO
from todo_rpg.application.exceptions import SessionNotFoundError


class GetCurrentUserTaskCategories:
    def __init__(
        self, repo: TaskCategoriesRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ):
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str) -> list[TaskCategoryDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_categories = await self.repo.get_current_user_task_categories(user_id)
        dtos = TaskCategoriesMapper.to_list_dto(task_categories)
        return dtos
