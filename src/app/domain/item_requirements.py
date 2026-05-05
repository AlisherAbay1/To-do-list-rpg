from uuid import UUID

from sqlalchemy import ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.app.infrastructure.database.models.base import Base

class ItemRequirements(Base, kw_only=True):
    __tablename__ = "item_requirements"
    __table_args__ = (UniqueConstraint("item_id", "skill_id", name="unique_item_skill"), )

    id: Mapped[UUID] = mapped_column(default_factory=uuid7, primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"))
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skill.id", ondelete="CASCADE"))
    required_lvl: Mapped[int] = mapped_column(BigInteger)