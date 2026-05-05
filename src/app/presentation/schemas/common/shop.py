from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ShopListingSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    item_id: UUID
    price: int
    quantity: int

class ShopListingShortSchemaRead(BaseModel):
    id: UUID
    item_id: UUID
    price: int
    quantity: int

class ShopListingSchemaCreate(BaseModel):
    item_id: UUID
    price: int = 0
    quantity: int = 1

class ShopListingSchemaUpdate(BaseModel):
    price: int | None = None
    quantity: int | None = None