from typing import Sequence, Optional
from uuid import UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy import desc, select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.domain.value_objects import TaskReward
from src.app.domain import Skill, Task, TaskHistory
from src.app.infrastructure.database.models.relations import \
    Tasks_history_to_skills

class TaskHistoryRepository:
    __slots__ = ("_session",)    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_recent_history_with_skills(self, task_id: UUID, limit: int) -> Sequence[TaskHistory]:
        task_history = select(
            TaskHistory
            ).where(
                TaskHistory.task_id == task_id
                ).order_by(
                    desc(TaskHistory.completed_at)
                    ).limit(
                        limit
                        ).options(
                            selectinload(TaskHistory.skills)
                        ).with_for_update()
        
        results = await self._session.scalars(task_history)
        return results.all()
    
    async def save_completion(self, task: Task, skills: Sequence[Skill], rewards: TaskReward) -> None:
        task_history = TaskHistory(
            user_id=task.user_id,
            task_id=task.id, 
            title=task.title, 
            xp_earned=rewards.xp, 
            gold_earned=rewards.gold
        )
        self._session.add(task_history)
        await self._session.flush()

        for skill in skills:
            skill_history = Tasks_history_to_skills(
                task_history_id=task_history.id, 
                skill_id=skill.id
            )
            self._session.add(skill_history)

    async def get_amount_of_total_completed_tasks(self, user_id: UUID) -> Optional[int]: 
        tasks_history = select(func.count()).select_from(TaskHistory).where(TaskHistory.user_id == user_id)
        result = await self._session.scalar(tasks_history)
        return result

    async def get_amount_of_today_completed_tasks(self, user_id: UUID) -> Optional[int]: 
        day_start = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        tasks_history = select(func.count()).select_from(TaskHistory).where(
            and_(
                TaskHistory.user_id == user_id, 
                TaskHistory.completed_at >= day_start, 
                TaskHistory.completed_at < day_end
                )
            )
        result = await self._session.scalar(tasks_history)
        return result

    async def get_amount_of_this_week_completed_tasks(self, user_id: UUID) -> Optional[int]: 
        date = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        date_data = date.isocalendar()
        week_start = date - timedelta(days=date_data.weekday - 1)
        week_end = week_start + timedelta(days=7)
        tasks_history = select(func.count()).select_from(TaskHistory).where(
            and_(
                TaskHistory.user_id == user_id, 
                TaskHistory.completed_at >= week_start, 
                TaskHistory.completed_at < week_end
                )
            )
        result = await self._session.scalar(tasks_history)
        return result