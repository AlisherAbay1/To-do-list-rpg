from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.app.domain.items import Item
from src.app.domain.skills import Skill
from src.app.infrastructure.database.models import Base


class ItemHistory(Base):
    __tablename__ = "item_usage_history"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    item_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("item.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255))
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))

    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_history_to_skills", lazy="noload")
    items: Mapped[list["Item"]] = relationship(secondary="tasks_history_to_items", lazy="noload")