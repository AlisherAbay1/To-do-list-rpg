from typing import Sequence
from uuid import UUID

from sqlalchemy import desc, select
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
                        )
        
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