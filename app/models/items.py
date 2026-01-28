from app.models import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid_utils import uuid7
from typing import Optional

class Item(Base):
    __tablename__ = "item"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    amount: Mapped[int]