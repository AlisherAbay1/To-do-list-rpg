from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.app.domain.skills import Skill
from src.app.domain.items import Item
from src.app.infrastructure.database.models.base import Base


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

    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_history_to_skills", lazy="noload")
    items: Mapped[list["Item"]] = relationship(secondary="tasks_history_to_items", lazy="noload")