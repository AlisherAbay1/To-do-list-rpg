from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from todo_rpg.domain.skills import Skill
from todo_rpg.domain.items import Item
from todo_rpg.infrastructure.database.models.base import Base


class TaskHistory(Base, kw_only=True):
    __tablename__ = "task_history"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    task_id: Mapped[UUID] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    xp_earned: Mapped[int] = mapped_column(BigInteger)
    gold_earned: Mapped[int] = mapped_column(BigInteger)

    skills: Mapped[list["Skill"]] = relationship(
        secondary="tasks_history_to_skills",
        lazy="noload",
        init=False,
        default_factory=list,
    )
    items: Mapped[list["Item"]] = relationship(
        secondary="tasks_history_to_items",
        lazy="noload",
        init=False,
        default_factory=list,
    )
