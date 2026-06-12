from todo_rpg.domain import Shop
from todo_rpg.application.dto import ShopListingDTO, ShopListingShortDTO
from typing import Sequence


class ShopMapper:
    @staticmethod
    def to_dto(domain: Shop) -> ShopListingDTO:
        dto = ShopListingDTO(
            id=domain.id,
            user_id=domain.user_id,
            item_id=domain.item_id,
            price=domain.price,
            quantity=domain.quantity,
        )
        return dto

    @staticmethod
    def to_list_dto(domains: Sequence[Shop]) -> list[ShopListingDTO]:
        return [ShopMapper.to_dto(domain) for domain in domains]

    @staticmethod
    def to_short_dto(domain: Shop) -> ShopListingShortDTO:
        dto = ShopListingShortDTO(
            id=domain.id,
            item_id=domain.item_id,
            price=domain.price,
            quantity=domain.quantity,
        )
        return dto

    @staticmethod
    def to_short_list_dto(domains: Sequence[Shop]) -> list[ShopListingShortDTO]:
        return [ShopMapper.to_short_dto(domain) for domain in domains]
