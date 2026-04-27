from datetime import datetime, timezone
from uuid import UUID

from src.app.application.exceptions import TaskNotFoundError
from src.app.application.interfaces.repositories_interfaces import \
    TaskRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol


class DeleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        task.deleted = True
        task.deleted_at = datetime.now(tz=timezone.utc)
        await self.repo.delete(task_id)
        await self.transaction.commit()
