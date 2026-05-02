from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol

class ClearExpiredTasksInteractor:
    def __init__(self, 
                 repo: TaskRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self) -> None:
        await self.repo.delete_all_tasks_deleted_more_than_year()
        await self.transaction.commit()