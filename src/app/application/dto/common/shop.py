from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class ShopListingDTO:
    id: UUID
    user_id: UUID
    item_id: UUID
    price: int
    quantity: int

@dataclass(slots=True)
class ShopListingShortDTO:
    id: UUID
    item_id: UUID
    price: int
    quantity: int

@dataclass(slots=True)
class ShopListingCreateDTO:
    item_id: UUID
    price: int
    quantity: int