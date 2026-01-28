from pydantic import UUID7, BaseModel, ConfigDict
from typing import Optional

class SkillSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int

    model_config = ConfigDict(from_attributes=True)

class SkillSchemaCreate(BaseModel):
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int

    model_config = ConfigDict(from_attributes=True)

