from src.app.application.interfaces.repositories_interfaces import InventoryRepositoryProtocol, ItemRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.mappers import ExtendedInventoryMapper 
from src.app.application.dto import InventoryShortWithItemDTO
from src.app.application.exceptions import (SessionNotFoundError, InventoryItemNotFoundError, 
                                            AccessDeniedError, ItemNotFoundError)
from uuid import UUID
from src.app.domain import ItemHistory

class UseCurrentUserInventoryItemInteractor:
    def __init__(self, 
                 inventory_repo: InventoryRepositoryProtocol, 
                 item_repo: ItemRepositoryProtocol,
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.inventory_repo = inventory_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, inventory_item_id: UUID) -> InventoryShortWithItemDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        inventory_item = await self.inventory_repo.get_inventory_item_by_id(inventory_item_id)
        if inventory_item is None:
            raise InventoryItemNotFoundError()
        if inventory_item.user_id != user_id:
            raise AccessDeniedError()
        
        if inventory_item.quantity > 1:
            inventory_item.quantity -= 1
        else: 
            inventory_item.quantity = 0
            await self.inventory_repo.delete(inventory_item)

        item = await self.item_repo.get_item_by_id(inventory_item.item_id)
        if item is None:
            raise ItemNotFoundError()
        
        item_usage_history = ItemHistory(
            user_id=user_id, 
            item_id=inventory_item.item_id, 
            title=item.title
        )

        await self.transaction.save(item_usage_history)

        dto = ExtendedInventoryMapper.to_inventory_item_with_item(inventory_item, item) 
        
        await self.transaction.commit()

        return dto