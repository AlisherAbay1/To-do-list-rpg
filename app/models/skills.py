from .base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("uuid_generate_v7()"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ico: Mapped[str] = mapped_column(nullable=True)
    lvl: Mapped[int]
    xp: Mapped[int]