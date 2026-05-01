from pydantic import BaseModel
from src.app.domain.enums import TaskRepeatFrequency, TaskDifficulty, TaskPriority, TaskType
from src.app.presentation.schemas.common.items import ItemSchemaRead
from src.app.presentation.schemas.common.skills import SkillSchemaRead
from src.app.presentation.schemas.common.users import UserSchemaRead
from typing import Optional
from datetime import datetime
from uuid import UUID

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