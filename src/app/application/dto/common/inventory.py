from dataclasses import dataclass
from uuid import UUID
from src.app.application.dto.sentinel_types import Unset, UNSET

@dataclass(slots=True)
class InventoryDTO:
    id: UUID
    user_id: UUID
    item_id: UUID
    quantity: int

@dataclass(slots=True)
class InventoryShortDTO:
    id: UUID
    item_id: UUID
    quantity: int

@dataclass(slots=True)
class InventoryCreateDTO:
    item_id: UUID
    quantity: int

@dataclass(slots=True)
class InventoryUpdateDTO:
    quantity: int | Unset = UNSET