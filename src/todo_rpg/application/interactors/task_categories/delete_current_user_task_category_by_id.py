from todo_rpg.application.interfaces import (
    TaskCategoriesRepositoryProtocol,
    UoWProtocol,
    SessionRepositoryProtocol,
)
from uuid import UUID
from todo_rpg.application.exceptions import SessionNotFoundError


class DeleteCurrentUserTaskCategoryByIdInteractor:
    def __init__(
        self,
        repo: TaskCategoriesRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, session_token: str, task_category_id: UUID) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        await self.repo.delete_current_user_task_category_by_id(
            task_category_id, user_id
        )
        await self.uow.commit()
