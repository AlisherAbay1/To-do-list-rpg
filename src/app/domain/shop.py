from dataclasses import dataclass, field
from uuid import UUID
from uuid6 import uuid7

@dataclass(kw_only=True)
class ShopDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    item_id: UUID
    price: int
    quantity: int

