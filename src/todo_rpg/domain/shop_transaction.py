from uuid import UUID

from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7
from datetime import datetime, timezone

from todo_rpg.infrastructure.database.models import Base


class ShopTransaction(Base, kw_only=True):
    __tablename__ = "shop_transaction"

    id: Mapped[UUID] = mapped_column(default_factory=uuid7, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    shop_listing_id: Mapped[UUID] = mapped_column(
        ForeignKey("shop.id", ondelete="SET NULL")
    )
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="SET NULL"))
    item_title: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(tz=timezone.utc)
    )
