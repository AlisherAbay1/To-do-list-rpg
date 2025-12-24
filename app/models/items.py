from .base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, ForeignKey

class Item(Base):
    __tablename__ = "item"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("uuid_generate_v7()"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    amount: Mapped[int]