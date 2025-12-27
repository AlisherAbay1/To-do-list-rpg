from pydantic import UUID7, BaseModel, ConfigDict
from typing import Optional

class SkillSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str
    description: str
    ico: str | None
    lvl: int
    xp: int

    model_config = ConfigDict(from_attributes=True)

class SkillSchemaCreate(BaseModel):
    title: str
    description: str
    ico: str | None
    lvl: int
    xp: int

    model_config = ConfigDict(from_attributes=True)

class SkillSchemaPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ico: Optional[str] = None
    lvl: Optional[int] = None
    xp: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)