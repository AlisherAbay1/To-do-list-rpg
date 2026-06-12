from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from uuid import UUID
from todo_rpg.application.exceptions import SessionNotFoundError


class DeleteCurrentUserTaskCategoryById:
    def __init__(
        self,
        repo: TaskCategoriesRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_id: str, task_category_id: UUID) -> None:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        await self.repo.delete_current_user_task_category_by_id(task_category_id)
        await self.uow.commit()
