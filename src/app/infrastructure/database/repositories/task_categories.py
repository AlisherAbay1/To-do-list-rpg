from sqlalchemy.ext.asyncio import AsyncSession
from src.app.domain import TaskCategory
from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy import delete, select


class TaskCategoriesRepository:
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_task_categories(self) -> Sequence[TaskCategory]:
        task_categories = select(TaskCategory)
        result = await self._session.scalars(task_categories)
        return result.all()

    async def get_current_user_task_categories(
        self, user_id: UUID
    ) -> Sequence[TaskCategory]:
        task_categories = select(TaskCategory).where(TaskCategory.user_id == user_id)
        result = await self._session.scalars(task_categories)
        return result.all()

    async def get_task_category_by_id(
        self, task_category_id: UUID
    ) -> Optional[TaskCategory]:
        task_category = (
            select(TaskCategory)
            .where(TaskCategory.id == task_category_id)
            .with_for_update()
        )
        result = await self._session.scalar(task_category)
        return result

    async def delete_current_user_task_category_by_id(
        self, task_category_id: UUID
    ) -> None:
        task_category = delete(TaskCategory).where(TaskCategory.id == task_category_id)
        await self._session.execute(task_category)
