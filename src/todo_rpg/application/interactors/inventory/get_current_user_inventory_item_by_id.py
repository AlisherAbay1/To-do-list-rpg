from todo_rpg.application.interfaces.repositories_interfaces import (
    InventoryRepositoryProtocol,
    ItemRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.mappers import ExtendedInventoryMapper
from todo_rpg.application.dto import InventoryShortWithItemDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    InventoryItemNotFoundError,
    AccessDeniedError,
    ItemNotFoundError,
)
from uuid import UUID


class GetCurrentUserInventoryItemByIdInteractor:
    def __init__(
        self,
        inventory_repo: InventoryRepositoryProtocol,
        item_repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.inventory_repo = inventory_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, inventory_item_id: UUID
    ) -> InventoryShortWithItemDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        inventory_item = await self.inventory_repo.get_inventory_item_by_id(
            inventory_item_id
        )
        if inventory_item is None:
            raise InventoryItemNotFoundError()
        if inventory_item.user_id != user_id:
            raise AccessDeniedError()
        item = await self.item_repo.get_item_by_id(inventory_item.item_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ExtendedInventoryMapper.to_inventory_item_with_item(inventory_item, item)
        return dto
