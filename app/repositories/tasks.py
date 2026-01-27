from app.models.tasks import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional, Sequence
from uuid import UUID

class TaskRepository:
    __slots__ = ("_session")
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_tasks(self, limit: int, offset: int) -> Sequence[Task]:
        tasks = select(Task).limit(limit).offset(offset)
        result = await self._session.scalars(tasks)
        return result.all()
    
    async def get_tasks_by_user_id(self, user_id: UUID, limit: int, offset: int) -> Sequence[Task]:
        tasks = select(Task).where(Task.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(tasks)
        return result.all()
    
    async def get_task_with_user(self, task_id: UUID) -> Optional[Task]:
        task_and_user = select(Task).options(joinedload(Task.user)).where(Task.id == task_id)
        result = await self._session.scalar(task_and_user)
        return result
    
    async def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        task = select(Task).where(Task.id == task_id)
        result = await self._session.scalar(task)
        return result

    def save(self, task: Task) -> None:
        self._session.add(task)

    async def delete(self, task: Task) -> None:
        await self._session.delete(task)