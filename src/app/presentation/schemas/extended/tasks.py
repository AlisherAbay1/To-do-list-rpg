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