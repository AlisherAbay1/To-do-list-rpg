from app.models import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Tasks_to_skills(Base):
    __tablename__ = "tasks_to_skills"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)

class Tasks_to_items(Base):
    __tablename__ = "tasks_to_items"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), primary_key=True)