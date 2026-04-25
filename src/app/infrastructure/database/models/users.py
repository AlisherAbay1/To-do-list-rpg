from src.app.infrastructure.database.models.base import Base
from uuid import UUID
from sqlalchemy import String, ForeignKey, BigInteger, Table, Column, UUID, Boolean
from uuid6 import uuid7

def get_user_table():
    user_table = Table(
        "user",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("username", String(25), unique=True),
        Column("email", String, unique=True),
        Column("password", String),
        Column("lvl", BigInteger, default=1),
        Column("xp", BigInteger, default=0),
        Column("is_admin", Boolean, default=False),
        Column("current_rank_id", UUID, ForeignKey("rank.id"), nullable=True, default=None),
        Column("profile_picture", String, nullable=True, default=None),
        Column("gold", BigInteger, default=0),
        Column("language", String(255), default="eng"),
        Column("timezone", String(255), default="UTC")
    )
    return user_table

def get_rank_table():
    rank_table = Table(
        "rank",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid7),
        Column("user_id", UUID, ForeignKey("user.id", ondelete="CASCADE")),
        Column("title", String(255))
    )
    return rank_table