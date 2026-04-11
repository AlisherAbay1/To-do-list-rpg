from dataclasses import dataclass, field
from typing import Optional, Literal
from uuid import UUID
from src.app.domain.enums import TaskRepeatFrequency, TaskType, TaskDifficulty, TaskPriority
from datetime import datetime
from src.app.presentation.schemas.sentinel_types import Unset, UNSET
from src.app.application.dto.items import ItemDTO
from src.app.application.dto.skills import SkillDTO

@dataclass(slots=True)
class TaskFilterParamsDTO:
    difficulty: Optional[TaskDifficulty] = None
    priority: Optional[TaskPriority] = None
    type: Optional[TaskType] = None
    repeat_frequency: Optional[TaskRepeatFrequency] = None
    deleted: Optional[bool] = None

@dataclass(slots=True)
class TaskSortParamsDTO:
    sort_by: Literal["difficulty", "priority", "deadline", "created_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "asc"

@dataclass(slots=True)
class TaskUpdateDTO:   
    title: str | Unset = UNSET
    description: str | None | Unset = UNSET
    category_id: UUID | None | Unset = UNSET
    repeat_limit: int | None | Unset = UNSET
    repeat_frequency: TaskRepeatFrequency | None | Unset = UNSET
    deadline: datetime | None | Unset = UNSET
    type: TaskType | None | Unset = UNSET
    difficulty: TaskDifficulty | None | Unset = UNSET
    priority: TaskPriority | None | Unset = UNSET
    custom_xp_reward: int | None | Unset = UNSET
    custom_gold_reward: int | None | Unset = UNSET
    deleted: bool | Unset = UNSET

@dataclass(slots=True)
class TaskDryDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]
    last_completed_at: Optional[datetime]
    created_at: datetime
    type: Optional[TaskType]
    difficulty: Optional[TaskDifficulty]
    priority: Optional[TaskPriority]
    custom_xp_reward: Optional[int]
    custom_gold_reward: Optional[int]


@dataclass(slots=True)
class TaskReward:
    xp: int
    gold: int

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

@dataclass(slots=True)
class TaskDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    xp: int
    gold: int
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]

@dataclass(slots=True)
class TaskCreateDTO:
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]
    type: Optional[TaskType] = None
    difficulty: Optional[TaskDifficulty] = None
    priority: Optional[TaskPriority] = None
    custom_xp_reward: Optional[int] = None
    custom_gold_reward: Optional[int] = None

    related_skills: list[UUID] = field(default_factory=list)
    related_items: list[UUID] = field(default_factory=list)