from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.app.infrastructure.database.models import Base


class UserRank(Base, kw_only=True):
    __tablename__ = "rank"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
