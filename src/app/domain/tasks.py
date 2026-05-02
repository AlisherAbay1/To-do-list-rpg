from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.app.domain.value_objects import TaskReward
from src.app.application.exceptions import (TaskAlreadyDoneError,
                                            TaskExecutedTooEarlyError)
from src.app.domain.enums import (TaskDifficulty, TaskPriority,
                                  TaskRepeatFrequency, TaskType)
from src.app.domain.items import Item
from src.app.domain.skills import Skill
from src.app.infrastructure.database.models.base import Base


class Task(Base, kw_only=True):
    __tablename__ = "task"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    category_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("task_category.id", ondelete="SET NULL"), default=None)
    repeat_limit: Mapped[Optional[int]] = mapped_column(default=None)
    repeat_frequency: Mapped[Optional[TaskRepeatFrequency]] = mapped_column(ENUM(TaskRepeatFrequency, name="repeat_frequency"), default=None)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)
    last_completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(tz=timezone.utc))
    type: Mapped[TaskType] = mapped_column(ENUM(TaskType, name="task_type"), default=TaskType.AUTO)
    difficulty: Mapped[Optional[TaskDifficulty]] = mapped_column(ENUM(TaskDifficulty, name="task_difficulty"))
    priority: Mapped[Optional[TaskPriority]] = mapped_column(ENUM(TaskPriority, name="task_priority"))
    custom_xp_reward: Mapped[Optional[int]] = mapped_column(BigInteger)
    custom_gold_reward: Mapped[Optional[int]] = mapped_column(BigInteger)
    deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)

    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_to_skills", lazy="noload", init=False, default_factory=list)
    items: Mapped[list["Item"]] = relationship(secondary="tasks_to_items", lazy="noload", init=False, default_factory=list)

    def complete(self):
        current_time = datetime.now(timezone.utc)
        if self.repeat_limit is not None:
            if self.repeat_limit == 0:
                raise TaskAlreadyDoneError()
            if self.repeat_limit > 0:
                self.repeat_limit -= 1
        if self.last_completed_at is not None:
            match self.repeat_frequency:
                case TaskRepeatFrequency.DAILY:
                    if current_time < self.last_completed_at + timedelta(days=1):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.ONCE_TWO_DAYS:
                    if current_time < self.last_completed_at + timedelta(days=2):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.WEEKLY:
                    if current_time < self.last_completed_at + timedelta(days=7):
                        raise TaskExecutedTooEarlyError()
        self.last_completed_at = current_time

    def calculate_task_rewards(self) -> TaskReward:
        xp = 0
        gold = 0
        if self.type == TaskType.AUTO:
            difficulty_multiplier, priority_multiplier = self._calculate_multipliers()
            xp = difficulty_multiplier * 60 + priority_multiplier * 40
            gold = difficulty_multiplier * 30 + priority_multiplier * 20
        elif self.type == TaskType.CUSTOM:
            if self.custom_xp_reward is not None:
                xp = self.custom_xp_reward
            if self.custom_gold_reward is not None:
                gold = self.custom_gold_reward
        return TaskReward(
                xp=xp, 
                gold=gold
            )

    def _calculate_multipliers(self): 
        match self.difficulty:
            case TaskDifficulty.EASY:
                difficulty_multiplier = 1
            case TaskDifficulty.MEDIUM:
                difficulty_multiplier = 2
            case TaskDifficulty.HARD:
                difficulty_multiplier = 3
            case TaskDifficulty.EPIC:
                difficulty_multiplier = 4
            case _: 
                difficulty_multiplier = 0
        match self.priority:
            case TaskPriority.LOW:
                priority_multiplier = 1
            case TaskPriority.MEDIUM:
                priority_multiplier = 2
            case TaskPriority.HIGH:
                priority_multiplier = 3
            case TaskPriority.CRITICAL:
                priority_multiplier = 4
            case _: 
                priority_multiplier = 0
        return difficulty_multiplier, priority_multiplier

    def delete(self) -> None:
        self.deleted = True
        self.deleted_at = datetime.now(tz=timezone.utc)