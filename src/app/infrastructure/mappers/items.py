from src.app.domain import ItemDomain
from src.app.infrastructure.database.models import Item
from typing import Sequence

class ItemMapper:
    @staticmethod
    def to_domain(orm: Item) -> ItemDomain:
        domain = ItemDomain(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            description=orm.description,
            deleted=orm.deleted,
            deleted_at=orm.deleted_at
        )
        return domain
    
    @staticmethod
    def to_domain_list(orms: Sequence[Item]) -> list[ItemDomain]:
        return [ItemMapper.to_domain(item) for item in orms]