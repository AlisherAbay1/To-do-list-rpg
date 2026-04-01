from dataclasses import dataclass, field
from typing import Optional, Literal
from uuid import UUID
from app.enums import TaskRepeatFrequency, TaskType, TaskDifficulty, TaskPriority
from datetime import datetime
from app.schemas.sentinel_types import Unset, UNSET

@dataclass(slots=True)
class UserDTO:
    username: str
    email: str
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID] = None
    profile_picture: Optional[str] = None

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
class SkillDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool = False
    deleted_at: Optional[datetime] = None

@dataclass(slots=True)
class ItemDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    deleted: bool = False
    deleted_at: Optional[datetime] = None

@dataclass(slots=True)
class CreateUserDTO:
    username: str
    email: str
    password: str

@dataclass(slots=True)
class LoginIdentifierDTO:
    username_or_email: str
    password: str

@dataclass(slots=True)
class CreateUserResultDTO:
    username: str
    email: str
    session_token: str

@dataclass(slots=True)
class UserEmailDTO:
    new_email: str
    password: str

@dataclass(slots=True)
class UserPasswordDTO:
    old_password: str
    new_password: str

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
class SkillCreateDTO:
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int

@dataclass(slots=True)
class SkillUpdateDTO:
    title: Optional[str]
    description: Optional[str]
    ico: Optional[str]
    lvl: Optional[int]
    xp: Optional[int]

@dataclass(slots=True)
class ItemUpdateDTO:
    title: Optional[str]
    description: Optional[str]


@dataclass(slots=True)
class ItemCreateDTO:
    title: str
    description: Optional[str]

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