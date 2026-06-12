from todo_rpg.domain import Inventory
from todo_rpg.application.dto import InventoryDTO, InventoryShortDTO
from typing import Sequence


class InventoryMapper:
    @staticmethod
    def to_dto(domain: Inventory) -> InventoryDTO:
        dto = InventoryDTO(
            id=domain.id,
            user_id=domain.user_id,
            item_id=domain.item_id,
            quantity=domain.quantity,
        )
        return dto

    @staticmethod
    def to_list_dto(domains: Sequence[Inventory]) -> list[InventoryDTO]:
        return [InventoryMapper.to_dto(domain) for domain in domains]

    @staticmethod
    def to_short_dto(domain: Inventory) -> InventoryShortDTO:
        dto = InventoryShortDTO(
            id=domain.id, item_id=domain.item_id, quantity=domain.quantity
        )
        return dto

    @staticmethod
    def to_short_list_dto(domains: Sequence[Inventory]) -> list[InventoryShortDTO]:
        return [InventoryMapper.to_short_dto(domain) for domain in domains]
