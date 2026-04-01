from app.models.base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, BigInteger
from uuid_utils import uuid7

class Inventory(Base):
    __tablename__ = "inventory"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), primary_key=True)
    quantity: Mapped[int] = mapped_column(BigInteger)