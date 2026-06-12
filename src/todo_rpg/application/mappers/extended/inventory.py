from todo_rpg.domain import Inventory, Item
from todo_rpg.application.dto import InventoryShortWithItemDTO
from todo_rpg.application.mappers import ItemMapper


class ExtendedInventoryMapper:
    @staticmethod
    def to_inventory_item_with_item(inventory_domain: Inventory, item_domain: Item):
        dto = InventoryShortWithItemDTO(
            id=inventory_domain.id,
            item_id=inventory_domain.item_id,
            quantity=inventory_domain.quantity,
            item=ItemMapper.to_dto(item_domain),
        )
        return dto
