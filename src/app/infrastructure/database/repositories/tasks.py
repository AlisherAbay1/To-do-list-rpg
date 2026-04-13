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
    
    async def get_task_by_id(self, task_id: UUID, get_related_skills: bool, get_related_items: bool) -> Optional[Task]:
        task = select(Task).where(Task.id == task_id)
        if get_related_skills:
            task = task.options(selectinload(Task.skills))
        if get_related_items:
            task = task.options(selectinload(Task.items))
        result = await self._session.scalar(task)
        return result

    async def get_task_with_user_and_skills(self, task_id: UUID) -> Optional[TaskDomain]:
        task_skills = select(
            Task
            ).where(
                Task.id == task_id
                ).options(
                    selectinload(Task.user),
                    selectinload(Task.skills)
                    )
        result = await self._session.scalar(task_skills)
        if result is None:
            return None
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
    
    async def save_completion(self, domain_task: TaskDomain) -> None:
        task = await self._session.get(
            Task, 
            domain_task.id, 
            options=[selectinload(Task.user), selectinload(Task.skills)]
            )
        if task is None:
            return 
        task.repeat_limit = domain_task.repeat_limit
        task.last_completed_at = domain_task.last_completed_at

        if task.user:
            task.user.xp = domain_task.user.xp
            task.user.lvl = domain_task.user.lvl
            task.user.gold = domain_task.user.gold

        domain_skills_map = {s.id: s for s in domain_task.skills}
        for orm_skill in task.skills:
            domain_skill = domain_skills_map.get(orm_skill.id)
            if domain_skill:
                orm_skill.xp = domain_skill.xp
                orm_skill.lvl = domain_skill.lvl