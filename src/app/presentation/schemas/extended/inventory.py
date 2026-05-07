from uuid import UUID
from pydantic import BaseModel
from src.app.presentation.schemas.common import ItemSchemaRead

class InventoryShortWithItemSchemaRead(BaseModel):
    id: UUID
    item_id: UUID
    quantity: int

    item: ItemSchemaRead