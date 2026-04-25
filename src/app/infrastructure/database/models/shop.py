from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import ForeignKey, BigInteger, Table, Column, UUID
from uuid6 import uuid7

def get_shop_table():
    shop_table = Table(
        "shop",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE")),
        Column("item_id", UUID, ForeignKey("item.id", ondelete="CASCADE")),
        Column("price", BigInteger),
        Column("quantity", BigInteger)
    )
    return shop_table