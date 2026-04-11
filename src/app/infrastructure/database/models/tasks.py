from src.app.infrastructure.database.models.base import Base
from src.app.infrastructure.database.models.users import User
from src.app.infrastructure.database.models.skills import Skill
from src.app.infrastructure.database.models.items import Item
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from src.app.domain.enums import TaskRepeatFrequency, TaskDifficulty, TaskPriority, TaskType
from uuid_utils import uuid7
from typing import Optional
from datetime import datetime, timezone

class Task(Base): 
    __tablename__ = "task"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    category_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("task_category.id", ondelete="SET NULL"), nullable=True)
    repeat_limit: Mapped[Optional[int]] = mapped_column(nullable=True, default=None)
    repeat_frequency: Mapped[Optional[TaskRepeatFrequency]] = mapped_column(ENUM(TaskRepeatFrequency, name="repeat_frequency"), nullable=True, default=None) 
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    last_completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    type: Mapped[Optional[TaskType]] = mapped_column(ENUM(TaskType, name="task_type"), default=TaskType.AUTO)
    difficulty: Mapped[Optional[TaskDifficulty]] = mapped_column(ENUM(TaskDifficulty, name="task_difficulty"), nullable=True)
    priority: Mapped[Optional[TaskPriority]] = mapped_column(ENUM(TaskPriority, name="task_priority"), nullable=True)
    custom_xp_reward: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    custom_gold_reward: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(passive_deletes=True, lazy="noload")
    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_to_skills", lazy="noload")
    items: Mapped[list["Item"]] = relationship(secondary="tasks_to_items", lazy="noload")

class TaskCategory(Base):
    __tablename__ = "task_category"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    color: Mapped[str] = mapped_column(String(255))

class TaskHistory(Base): 
    __tablename__ = "task_history"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    task_id: Mapped[UUID] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    xp_earned: Mapped[int] = mapped_column(BigInteger)
    gold_earned: Mapped[int] = mapped_column(BigInteger)

    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_history_to_skills", lazy="noload")