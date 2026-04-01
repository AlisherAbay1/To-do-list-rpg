from app.models.base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, String
from uuid_utils import uuid7
from typing import Optional
from datetime import datetime, timezone

class Item(Base):
    __tablename__ = "item"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
class ItemUsageHistory(Base):
    __tablename__ = "item_usage_history"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255))
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))