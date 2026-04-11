from pydantic import UUID7, BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ItemSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str
    description: Optional[str]
    deleted: bool
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ItemSchemaCreate(BaseModel):
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

