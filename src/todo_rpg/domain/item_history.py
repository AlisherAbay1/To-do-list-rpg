from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from todo_rpg.infrastructure.database.models import Base


class ItemHistory(Base, kw_only=True):
    __tablename__ = "item_usage_history"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    item_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("item.id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(String(255))
    used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(tz=timezone.utc)
    )
