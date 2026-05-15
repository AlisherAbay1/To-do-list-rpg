from uuid import UUID

from src.app.application.exceptions import TaskNotFoundError, SessionNotFoundError
from src.app.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol


class DeleteCurrentUserTaskInteractor:
    def __init__(
        self,
        repo: TaskRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, task_id: UUID):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task = await self.repo.get_task_by_id(task_id, user_id)
        if task is None:
            raise TaskNotFoundError()
        task.delete()
        await self.transaction.commit()
