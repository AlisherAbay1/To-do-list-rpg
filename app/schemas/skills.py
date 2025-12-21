from pydantic import UUID7, BaseModel, ConfigDict

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
    user_id: UUID7
    title: str
    description: str
    ico: str | None
    lvl: int
    xp: int

    model_config = ConfigDict(from_attributes=True)