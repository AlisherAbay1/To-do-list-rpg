from todo_rpg.application.interfaces import (
    TaskCategoriesRepositoryProtocol,
    SessionRepositoryProtocol,
)
from todo_rpg.application.mappers.common import TaskCategoriesMapper
from todo_rpg.application.dto import TaskCategoryDTO
from todo_rpg.application.exceptions import SessionNotFoundError


class GetCurrentUserTaskCategoriesInteractor:
    def __init__(
        self,
        repo: TaskCategoriesRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
    ):
        self.repo = repo
        self.session_repo = session_repo

    async def __call__(self, session_token: str) -> list[TaskCategoryDTO]:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_categories = await self.repo.get_current_user_task_categories(user_id)
        dtos = TaskCategoriesMapper.to_list_dto(task_categories)
        return dtos
