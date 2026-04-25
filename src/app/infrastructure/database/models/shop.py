from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import ForeignKey, BigInteger, Table, Column, UUID
from uuid6 import uuid7

def get_shop_table():
    shop_table = Table(
        "shop",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        Column("item_id", UUID, ForeignKey("item.id", ondelete="CASCADE"), nullable=False),
        Column("price", BigInteger, nullable=False),
        Column("quantity", BigInteger, nullable=False)
    )
    return shop_table