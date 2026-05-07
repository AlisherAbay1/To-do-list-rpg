from uuid import UUID
from dataclasses import dataclass
from src.app.application.dto import ItemDTO

@dataclass(slots=True)
class InventoryShortWithItemDTO:
    id: UUID
    item_id: UUID
    quantity: int

    item: ItemDTO