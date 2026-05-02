from typing import Optional
from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.app.domain.value_objects import TaskReward
from src.app.infrastructure.database.models.base import Base


class User(Base, kw_only=True):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    lvl: Mapped[int] = mapped_column(BigInteger, default=1)
    xp: Mapped[int] = mapped_column(BigInteger, default=0)
    is_admin: Mapped[bool] = mapped_column(default=False)
    current_rank_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("rank.id", use_alter=True), default=None)
    profile_picture: Mapped[Optional[str]] = mapped_column(default=None)
    gold: Mapped[int] = mapped_column(BigInteger, default=0)
    language: Mapped[str] = mapped_column(String(255), default="eng")
    timezone: Mapped[str] = mapped_column(String(255), default="UTC")

    def apply_rewards(self, rewards: TaskReward):
        self.xp += rewards.xp
        self.lvl = self.calculate_lvl(rewards.xp)
        self.gold += rewards.gold

    def calculate_lvl(self, xp: int):
        return 1 + xp // 1000