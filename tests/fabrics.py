from uuid import UUID
from typing import Optional
from src.app.domain.enums import (TaskDifficulty, TaskPriority,
                                  TaskRepeatFrequency, TaskType)
from datetime import datetime, timezone
from src.app.domain import Task
from  uuid6 import uuid7

def make_task(
    user_id: Optional[UUID] = None,
    title: str = "Test task",
    description: Optional[str] = None,
    category_id: Optional[UUID] = None,
    repeat_limit: Optional[int] = None,
    repeat_frequency: Optional[TaskRepeatFrequency] = None,
    deadline: Optional[datetime] = None,
    last_completed_at: Optional[datetime] = None,
    created_at: Optional[datetime] = None,
    type: TaskType = TaskType.AUTO,
    difficulty: Optional[TaskDifficulty] = None,
    priority: Optional[TaskPriority] = None,
    custom_xp_reward: Optional[int] = None,
    custom_gold_reward: Optional[int] = None,
    deleted: bool = False,
    deleted_at: Optional[datetime] = None,
) -> Task:
    return Task(
        user_id=user_id or uuid7(),
        title=title,
        description=description,
        category_id=category_id,
        repeat_limit=repeat_limit,
        repeat_frequency=repeat_frequency,
        deadline=deadline,
        last_completed_at=last_completed_at,
        created_at=created_at or datetime.now(tz=timezone.utc),
        type=type,
        difficulty=difficulty,
        priority=priority,
        custom_xp_reward=custom_xp_reward,
        custom_gold_reward=custom_gold_reward,
        deleted=deleted,
        deleted_at=deleted_at,
    )