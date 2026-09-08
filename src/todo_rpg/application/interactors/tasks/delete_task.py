from uuid import UUID

from todo_rpg.application.exceptions import TaskNotFoundError, SessionNotFoundError
from todo_rpg.application.interfaces import (
    TaskRepositoryProtocol,
    UoWProtocol,
    RedisRepositoryProtocol,
)


class DeleteCurrentUserTaskInteractor:
    def __init__(
        self,
        repo: TaskRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, task_id: UUID) -> None:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task = await self.repo.get_task_by_id(task_id, user_id)
        if task is None:
            raise TaskNotFoundError()
        task.delete()
        await self.uow.commit()
