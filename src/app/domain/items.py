from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.app.domain.item_requirements import ItemRequirement
from src.app.infrastructure.database.models.base import Base


class Item(Base, kw_only=True):
    __tablename__ = "item"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)

    requirements: Mapped[list["ItemRequirement"]] = relationship(lazy="noload", init=False, default_factory=list)

    def delete(self) -> None:
        self.deleted = True
        self.deleted_at = datetime.now(tz=timezone.utc)