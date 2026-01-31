from app.models.base import Base
from app.models.skills import Skill
from app.models.items import Item
from uuid import UUID
from sqlalchemy import String, ForeignKey, text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    current_rank_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, default=None)
    profile_picture: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)

    # relationships
    skills: Mapped[list["Skill"]] = relationship(passive_deletes=True)
    items: Mapped[list["Item"]] = relationship(passive_deletes=True)
    ranks: Mapped[list["Rank"]] = relationship(passive_deletes=True)

class Rank(Base):
    __tablename__ = "rank"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[Optional[str]] = mapped_column(nullable=True)