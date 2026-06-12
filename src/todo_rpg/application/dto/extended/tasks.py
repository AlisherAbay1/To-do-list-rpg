from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from todo_rpg.application.dto.common.items import ItemDTO
from todo_rpg.application.dto.common.skills import SkillDTO
from todo_rpg.application.dto.common.users import UserDTO
from todo_rpg.domain.enums.task_types import (
    TaskDifficulty,
    TaskPriority,
    TaskRepeatFrequency,
    TaskType,
)


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
    last_completed_at: Optional[datetime]
    type: Optional[TaskType]
    difficulty: Optional[TaskDifficulty]
    priority: Optional[TaskPriority]
    custom_xp_reward: Optional[int]
    custom_gold_reward: Optional[int]
    deleted: bool
    deleted_at: Optional[datetime]

    skills: list[SkillDTO]
    items: list[ItemDTO]
