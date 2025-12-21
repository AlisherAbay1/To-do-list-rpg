from pydantic import UUID7, BaseModel, ConfigDict
from app.enums import RepeatTypes

class TaskSchemaRead(BaseModel):   
    id: UUID7
    user_id: UUID7
    title: str
    description: str
    xp: int
    is_done: bool
    repeat_limit: int
    repeat_type: RepeatTypes

    model_config = ConfigDict(from_attributes=True)

class TaskSchemaCreate(BaseModel): 
    user_id: UUID7
    title: str
    description: str
    xp: int
    is_done: bool
    repeat_limit: int
    repeat_type: RepeatTypes | None

    model_config = ConfigDict(from_attributes=True)