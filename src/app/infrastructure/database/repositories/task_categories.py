from sqlalchemy.ext.asyncio import AsyncSession
from src.app.domain import TaskCategory
from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy import delete, select

class TaskCategoriesRepository:
    __slots__ = ("_session", )
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_task_categories(self) -> Sequence[TaskCategory]:
        task_categories = select(
            TaskCategory
        )
        result = await self._session.scalars(task_categories)
        return result.all()