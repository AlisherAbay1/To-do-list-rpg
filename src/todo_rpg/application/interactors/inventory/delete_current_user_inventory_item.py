from todo_rpg.application.interfaces.repositories_interfaces import (
    InventoryRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    InventoryItemNotFoundError,
    AccessDeniedError,
)
from uuid import UUID


class DeleteCurrentUserInventoryItemInteractor:
    def __init__(
        self,
        repo: InventoryRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, inventory_item_id: UUID, session_token: str) -> None:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        inventory_item = await self.repo.get_inventory_item_by_id(inventory_item_id)
        if inventory_item is None:
            raise InventoryItemNotFoundError()
        if inventory_item.user_id != user_id:
            raise AccessDeniedError()
        await self.repo.delete(inventory_item)
        await self.transaction.commit()
