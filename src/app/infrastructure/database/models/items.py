from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import ForeignKey, DateTime, String, Table, Column, UUID, Boolean
from uuid6 import uuid7
from datetime import datetime, timezone

def get_item_table():
    item_table = Table(
        "item",
        Base.metadata, 
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        Column("title", String(255), nullable=False),
        Column("description", String, nullable=True, default=None),
        Column("deleted", Boolean, default=False, nullable=False),
        Column("deleted_at", DateTime(timezone=True), nullable=True, default=None)
    )
    return item_table

def get_item_usage_history_table():
    item_usage_history_table = Table(
        "item_usage_history",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        Column("item_id", UUID, ForeignKey("item.id", ondelete="SET NULL"), nullable=True),
        Column("title", String(255), nullable=False),
        Column("used_at", DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    )
    return item_usage_history_table