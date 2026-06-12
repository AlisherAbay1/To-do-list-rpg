from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from todo_rpg.presentation.schemas import TaskSchemaReadable


class SkillWithTasksAndNextLvlXpSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]

    xp_for_next_lvl: int

    tasks: list[TaskSchemaReadable]
