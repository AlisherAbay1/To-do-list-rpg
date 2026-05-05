from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ItemSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    deleted: bool
    deleted_at: Optional[datetime]

class ItemSchemaCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ItemSchemaUpdate(BaseModel):
    title: str | None = None
    description: Optional[str] = None