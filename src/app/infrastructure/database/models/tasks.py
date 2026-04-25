from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, BigInteger, DateTime, Table, Column, UUID, Integer, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from src.app.domain.enums import TaskRepeatFrequency, TaskDifficulty, TaskPriority, TaskType
from uuid6 import uuid7
from datetime import datetime, timezone

def get_task_table():
    task_table = Table(
        "task",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE")),
        Column("title", String(255)),
        Column("description", String, nullable=True, default=None),
        Column("category_id", UUID, ForeignKey("task_category.id", ondelete="SET NULL"), nullable=True, default=None),
        Column("repeat_limit", Integer, nullable=True, default=None),
        Column("repeat_frequency", ENUM(TaskRepeatFrequency, name="repeat_frequency"), nullable=True, default=None),
        Column("deadline", DateTime(timezone=True), nullable=True, default=None),
        Column("last_completed_at", DateTime(timezone=True), nullable=True, default=None),
        Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)),
        Column("type", ENUM(TaskType, name="task_type"), default=TaskType.AUTO),
        Column("difficulty", ENUM(TaskDifficulty, name="task_difficulty"), nullable=True),
        Column("priority", ENUM(TaskPriority, name="task_priority"), nullable=True),
        Column("custom_xp_reward", BigInteger, nullable=True),
        Column("custom_gold_reward", BigInteger, nullable=True),
        Column("deleted", Boolean, default=False),
        Column("deleted_at", DateTime(timezone=True), nullable=True, default=None)
    )
    return task_table

def get_task_category_table():
    task_category_table = Table(
        "task_category",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE")),
        Column("title", String(255)),
        Column("color", String(255))
    )
    return task_category_table

def get_task_history_table():
    task_history_table = Table(
        "task_history",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE")),
        Column("task_id", UUID, ForeignKey("task.id", ondelete="CASCADE")),
        Column("title", String(255)),
        Column("completed_at", DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)),
        Column("xp_earned", BigInteger),
        Column("gold_earned", BigInteger)
    )
    return task_history_table