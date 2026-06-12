from dataclasses import dataclass
from uuid import UUID
from todo_rpg.application.dto.sentinel_types import Unset, UNSET


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


@dataclass(slots=True)
class ShopListingUpdateDTO:
    price: int | Unset = UNSET
    quantity: int | Unset = UNSET
