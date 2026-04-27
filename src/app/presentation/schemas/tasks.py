from pydantic import BaseModel, ConfigDict
from src.app.domain.enums import TaskRepeatFrequency, TaskDifficulty, TaskPriority, TaskType
from src.app.presentation.schemas.items import ItemSchemaRead
from src.app.presentation.schemas.skills import SkillSchemaRead
from src.app.presentation.schemas.users import UserSchemaRead
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

class TaskSchemaRead(BaseModel):   
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
    deleted: bool
    deleted_at: Optional[datetime]

class TaskSchemaReadable(BaseModel):
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

class TaskWithUserAndSkillsSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    category_id: Optional[UUID]
    xp: int
    gold: int
    repeat_limit: Optional[int]
    repeat_frequency: Optional[TaskRepeatFrequency]
    deadline: Optional[datetime]

    user: UserSchemaRead
    skills: list[SkillSchemaRead]

class TaskWithSkillsAndItemsSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    repeat_limit: Optional[int] = None
    repeat_frequency: Optional[TaskRepeatFrequency] = None
    deadline: Optional[datetime] = None
    last_completed_at: Optional[datetime] = None
    created_at: datetime
    type: Optional[TaskType] = None
    difficulty: Optional[TaskDifficulty] = None
    priority: Optional[TaskPriority] = None
    custom_xp_reward: Optional[int] = None
    custom_gold_reward: Optional[int] = None
    deleted: bool = False
    deleted_at: Optional[datetime] = None

    skills: list[SkillSchemaRead] = []
    items: list[ItemSchemaRead] = []

    model_config = ConfigDict(from_attributes=True)

class TaskFilterParams(BaseModel):
    difficulty: Optional[TaskDifficulty] = None
    priority: Optional[TaskPriority] = None
    type: Optional[TaskType] = None
    repeat_frequency: Optional[TaskRepeatFrequency] = None
    deleted: Optional[bool] = None

class TaskSortParams(BaseModel):
    sort_by: Literal["difficulty", "priority", "deadline", "created_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "asc"

class TaskSchemaCreate(BaseModel): 
    title: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    repeat_limit: Optional[int] = None
    repeat_frequency: Optional[TaskRepeatFrequency] = None
    deadline: Optional[datetime] = None
    type: Optional[TaskType] = None
    difficulty: Optional[TaskDifficulty] = None
    priority: Optional[TaskPriority] = None
    custom_xp_reward: Optional[int] = None
    custom_gold_reward: Optional[int] = None

    related_skills: list[UUID] = []
    related_items: list[UUID] = []

class TaskSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: UUID | None = None
    repeat_limit: int | None = None
    repeat_frequency: TaskRepeatFrequency | None = None
    deadline: datetime | None = None
    type: TaskType | None = None
    difficulty: TaskDifficulty | None = None
    priority: TaskPriority | None = None
    custom_xp_reward: int | None = None
    custom_gold_reward: int | None = None
    deleted: bool | None = None