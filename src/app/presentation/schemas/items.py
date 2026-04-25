from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class ItemSchemaCreate(BaseModel):
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

