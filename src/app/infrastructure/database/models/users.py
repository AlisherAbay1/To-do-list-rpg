from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, BigInteger, Table, Column, UUID, Boolean
from uuid6 import uuid7

def get_user_table():
    user_table = Table(
        "user",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("username", String(25), unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("password", String, nullable=False),
        Column("lvl", BigInteger, default=1, nullable=False),
        Column("xp", BigInteger, default=0, nullable=False),
        Column("is_admin", Boolean, default=False, nullable=False),
        Column("current_rank_id", UUID, ForeignKey("rank.id", use_alter=True), nullable=True, default=None),
        Column("profile_picture", String, nullable=True, default=None),
        Column("gold", BigInteger, default=0, nullable=False),
        Column("language", String(255), default="eng", nullable=False),
        Column("timezone", String(255), default="UTC", nullable=False)
    )
    return user_table

def get_rank_table():
    rank_table = Table(
        "rank",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        Column("title", String(255), nullable=False)
    )
    return rank_table