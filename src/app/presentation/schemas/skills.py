from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class SkillSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class SkillSchemaCreate(BaseModel):
    title: str
    description: Optional[str]
    ico: Optional[str] = None
    lvl: int = 1
    xp: int = 0

    model_config = ConfigDict(from_attributes=True)

