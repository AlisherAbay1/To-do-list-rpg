from app.models import Base
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
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ico: Mapped[Optional[str]] = mapped_column(nullable=True)
    lvl: Mapped[int]
    xp: Mapped[int]