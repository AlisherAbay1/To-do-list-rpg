from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, DateTime, Column, Table, UUID, Integer, Boolean
from uuid6 import uuid7

def get_skill_table():
    skill_table = Table(
        "skill",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        Column("title", String(255), nullable=False),
        Column("description", String, nullable=True, default=None),
        Column("ico", String, nullable=True, default=None),
        Column("lvl", Integer, default=1, nullable=False),
        Column("xp", Integer, default=0, nullable=False),
        Column("deleted", Boolean, default=False, nullable=False),
        Column("deleted_at", DateTime(timezone=True), nullable=True, default=None)
    )
    return skill_table