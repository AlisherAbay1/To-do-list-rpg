from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from todo_rpg.infrastructure.database.models.base import Base


class Shop(Base, kw_only=True):
    __tablename__ = "shop"
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="unique_user_item_for_shop"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"))
    price: Mapped[int] = mapped_column(BigInteger)
    quantity: Mapped[int] = mapped_column(BigInteger)
