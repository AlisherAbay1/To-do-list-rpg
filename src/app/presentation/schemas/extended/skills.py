from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.app.presentation.schemas import TaskSchemaReadable

class SkillWithTasksSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]

    tasks: list[TaskSchemaReadable]