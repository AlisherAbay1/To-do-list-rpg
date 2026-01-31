from app.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid_utils import uuid7
from typing import Optional

class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    ico: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    lvl: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)