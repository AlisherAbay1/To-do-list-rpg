from src.app.infrastructure.database.models.base import Base
from sqlalchemy import ForeignKey, BigInteger, Table, Column, UUID

def get_inventory_table():
    inventory_table = Table(
        "inventory",
        Base.metadata, 
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
        Column("item_id", UUID, ForeignKey("item.id", ondelete="CASCADE"), primary_key=True),
        Column("quantity", BigInteger, nullable=False)
    )
    return inventory_table