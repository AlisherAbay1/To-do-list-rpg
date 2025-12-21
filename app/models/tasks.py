from .base import Base, UUID
from .skills import Skill
from .users import User
from .items import Item
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, text, BigInteger
from sqlalchemy.dialects.postgresql import ENUM
from app.enums import RepeatTypes

class Task(Base): 
    __tablename__ = "task"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("uuid_generate_v7()"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    xp: Mapped[int] = mapped_column(BigInteger)
    is_done: Mapped[bool] = mapped_column(default=False)
    repeat_limit: Mapped[int | None] = mapped_column(nullable=True)
    repeat_type: Mapped[RepeatTypes] = mapped_column(ENUM(RepeatTypes, name="repeat_types"), nullable=True) 

    # relationships
    user: Mapped["User"] = relationship(passive_deletes=True)
    skills: Mapped[list["Skill"]] = relationship(secondary="tasks_to_skills", passive_deletes=True)
    items: Mapped[list["Item"]] = relationship(secondary="tasks_to_items", passive_deletes=True)

