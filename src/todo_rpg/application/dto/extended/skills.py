from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime
from todo_rpg.application.dto.common import TaskDTO


@dataclass(slots=True)
class SkillWithTasksAndNextLvlXpDTO:
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

    tasks: list[TaskDTO]
