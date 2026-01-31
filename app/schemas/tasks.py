from pydantic import UUID7, BaseModel, ConfigDict
from app.enums import RepeatTypes
from typing import Optional

class TaskSchemaRead(BaseModel):   
    id: UUID7
    user_id: UUID7
    title: str
    description: Optional[str]
    xp: int
    is_done: bool
    repeat_limit: int
    repeat_type: Optional[RepeatTypes] 

    model_config = ConfigDict(from_attributes=True)

class TaskSchemaCreate(BaseModel): 
    title: str
    description: Optional[str]
    xp: int = 0
    is_done: bool = False
    repeat_limit: int = 1
    repeat_type: Optional[RepeatTypes] = None

    model_config = ConfigDict(from_attributes=True)

