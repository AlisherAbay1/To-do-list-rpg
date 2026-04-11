from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import TaskNotFoundError
from uuid import UUID
from datetime import datetime, timezone

class DeleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id, get_related_skills=False, get_related_items=False)
        if task is None:
            raise TaskNotFoundError()
        task.deleted = True
        task.deleted_at = datetime.now(tz=timezone.utc)
        await self.transaction.delete(task)
        await self.transaction.commit()
