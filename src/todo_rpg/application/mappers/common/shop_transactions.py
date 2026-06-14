from typing import Sequence

from todo_rpg.application.dto import ShopTransactionDTO
from todo_rpg.domain import ShopTransaction


class ShopTransactionMapper:
    @staticmethod
    def to_dto(domain: ShopTransaction) -> ShopTransactionDTO:
        return ShopTransactionDTO(
            id=domain.id,
            user_id=domain.user_id,
            shop_listing_id=domain.shop_listing_id,
            item_id=domain.item_id,
            item_title=domain.item_title,
            price=domain.price,
            date=domain.date,
        )

    @staticmethod
    def to_list_dto(domains: Sequence[ShopTransaction]) -> list[ShopTransactionDTO]:
        return [ShopTransactionMapper.to_dto(domain) for domain in domains]
