from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime
from src.app.application.dto import TaskDTO

@dataclass(slots=True)
class SkillWithTasksDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]

    tasks: list[TaskDTO]