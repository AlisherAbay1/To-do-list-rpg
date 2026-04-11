from pydantic import UUID7, BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SkillSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
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

