from src.app.application.interfaces.repositories_interfaces import ItemRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from uuid import UUID

class DeleteItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, item_id: UUID):
        await self.repo.delete(item_id)
        await self.transaction.commit()