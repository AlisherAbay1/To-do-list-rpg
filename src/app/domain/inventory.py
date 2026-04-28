from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.app.infrastructure.database.models.base import Base


class Inventory(Base, kw_only=True):
    __tablename__ = "inventory"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), primary_key=True)
    quantity: Mapped[int] = mapped_column(BigInteger)