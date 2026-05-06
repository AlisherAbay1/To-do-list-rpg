from uuid import UUID
from uuid6 import uuid7

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.app.infrastructure.database.models.base import Base


class Inventory(Base, kw_only=True):
    __tablename__ = "inventory"

    id: Mapped[UUID] = mapped_column(default_factory=uuid7, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(BigInteger)