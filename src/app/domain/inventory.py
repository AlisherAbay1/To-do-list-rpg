from dataclasses import dataclass
from uuid import UUID

@dataclass(kw_only=True)
class InventoryDomain:
    user_id: UUID
    item_id: UUID
    quantity: int