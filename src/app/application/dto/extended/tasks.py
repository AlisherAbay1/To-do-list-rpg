from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.app.application.dto.common.items import ItemDTO
from src.app.application.dto.common.skills import SkillDTO
from src.app.application.dto.common.users import UserDTO
from src.app.domain.enums.task_types import TaskDifficulty, TaskPriority, TaskRepeatFrequency, TaskType

@dataclass(slots=True)
class TaskWithUserAndSkillsDTO:
    id: UUID
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    xp: int
    gold: int
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]

    user: UserDTO
    skills: list[SkillDTO]

@dataclass(slots=True)
class TaskWithSkillsAndItemsDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]
    created_at: datetime
    type: Optional[TaskType]
    difficulty: Optional[TaskDifficulty]
    priority: Optional[TaskPriority]
    custom_xp_reward: Optional[int]
    custom_gold_reward: Optional[int]

    skills: list[SkillDTO]
    items: list[ItemDTO]