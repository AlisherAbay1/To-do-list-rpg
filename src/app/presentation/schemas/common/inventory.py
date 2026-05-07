from uuid import UUID
from pydantic import BaseModel

class InventorySchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    item_id: UUID
    quantity: int

class InventoryShortSchemaRead(BaseModel):
    id: UUID
    item_id: UUID
    quantity: int