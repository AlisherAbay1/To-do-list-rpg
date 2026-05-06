from dataclasses import dataclass
from uuid import UUID
from src.app.application.dto.sentinel_types import Unset, UNSET

@dataclass(slots=True)
class InventoryDTO:
    id: UUID
    