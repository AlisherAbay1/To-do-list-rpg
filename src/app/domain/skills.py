from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.app.infrastructure.database.models.base import Base

class Skill(Base, kw_only=True):
    __tablename__ = "skill"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    ico: Mapped[Optional[str]] = mapped_column(default=None)
    lvl: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)
    deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)

    def apply_reward(self, xp: int):
        self.xp += xp
        self.lvl = self.xp // 1000