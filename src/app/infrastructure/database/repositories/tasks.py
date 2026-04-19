from src.app.infrastructure.database.models.tasks import Task
from src.app.infrastructure.mappers import TaskMapper
from src.app.domain import TaskDomain
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional, Sequence
from uuid import UUID
from src.app.application.dto.tasks import TaskFilterParamsDTO, TaskSortParamsDTO
from src.app.domain.enums import TaskRepeatFrequency

class TaskRepository:
    __slots__ = ("_session",)
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_tasks(self, filters: TaskFilterParamsDTO, sorting: TaskSortParamsDTO, limit: int, offset: int) -> Sequence[Task]:
        tasks = select(Task).limit(limit).offset(offset)
        if filters.type is not None:
            tasks = tasks.where(Task.type == filters.type)
        if filters.priority is not None:
            tasks = tasks.where(Task.priority == filters.priority)
        if filters.difficulty is not None:
            tasks = tasks.where(Task.difficulty == filters.difficulty)
        if filters.repeat_frequency is not None:
            tasks = tasks.where(Task.repeat_frequency == filters.repeat_frequency)
        if filters.deleted is not None:
            tasks = tasks.where(Task.deleted == filters.deleted)

        if sorting.sort_order == "asc":
            if sorting.sort_by == "difficulty":
                tasks = tasks.order_by(Task.difficulty)
            if sorting.sort_by == "priority":
                tasks = tasks.order_by(Task.priority)
            if sorting.sort_by == "deadline":
                tasks = tasks.order_by(Task.deadline)
            if sorting.sort_by == "created_at":
                tasks = tasks.order_by(Task.created_at)
        if sorting.sort_order == "desc":
            if sorting.sort_by == "difficulty":
                tasks = tasks.order_by(desc(Task.difficulty))
            if sorting.sort_by == "priority":
                tasks = tasks.order_by(desc(Task.priority))
            if sorting.sort_by == "deadline":
                tasks = tasks.order_by(desc(Task.deadline))
            if sorting.sort_by == "created_at":
                tasks = tasks.order_by(desc(Task.created_at))
                
        result = await self._session.scalars(tasks)
        return result.all()
    
    async def get_deleted_tasks_by_user_id(self, user_id: UUID) -> Sequence[Task]:
        tasks = select(
            Task
            ).where(
                and_(Task.user_id == user_id, 
                     Task.deleted == True
                     )
                    )
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
    
    async def get_task_by_id(self, task_id: UUID, get_related_skills: bool = False, get_related_items: bool = False) -> Optional[TaskDomain]:
        task = select(Task).where(Task.id == task_id)
        if get_related_skills:
            task = task.options(selectinload(Task.skills))
        if get_related_items:
            task = task.options(selectinload(Task.items))
        result = await self._session.scalar(task)
        if result is None: 
            return
        return TaskMapper.to_domain(result)
    
    async def get_daily_tasks_by_user_id(self, user_id: UUID) -> Sequence[Task]: 
        tasks = select(
            Task
            ).where(
                and_(
                    Task.user_id == user_id, 
                    Task.repeat_frequency == TaskRepeatFrequency.DAILY
                    )
                )
        result = await self._session.scalars(tasks)
        return result.all()
    
    async def update(self, domain: TaskDomain) -> None:
        task = await self._session.get(Task, domain.id)
        if task is None:
            return 
        TaskMapper.update_orm(domain, task)