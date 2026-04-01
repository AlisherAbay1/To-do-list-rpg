from app.models.tasks import TaskHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from typing import Optional, Sequence
from uuid import UUID

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
                        )
        
        results = await self._session.scalars(task_history)
        return results.all()