from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from uuid_utils import uuid7
from typing import Optional

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    lvl: Mapped[int] = mapped_column(BigInteger, default=1)
    xp: Mapped[int] = mapped_column(BigInteger, default=0)
    is_admin: Mapped[bool] = mapped_column(default=False)
    current_rank_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("rank.id"), nullable=True, default=None)
    profile_picture: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    gold: Mapped[int] = mapped_column(BigInteger, default=0)
    language: Mapped[str] = mapped_column(String(255), default="eng")
    timezone: Mapped[str] = mapped_column(String(255), default="UTC")

class Rank(Base):
    __tablename__ = "rank"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))