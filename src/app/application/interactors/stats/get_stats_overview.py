from src.app.application.interfaces.repositories_interfaces import (UserRepositoryProtocol, 
                                                                    TaskRepositoryProtocol, 
                                                                    SkillRepositoryProtocol, 
                                                                    TaskHistoryRepositoryProtocol)
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError, UserNotFoundError
from src.app.application.mappers import StatsMapper
from src.app.application.dto import StatsOverviewDTO

"""
- User: level, xp, xp_to_next_level, money
- Tasks: total_completed, completed_today, completed_this_week, overdue_count
- Skills: top skills by level
"""

class GetStatsOverviewInteractor:
    def __init__(self, 
                 user_repo: UserRepositoryProtocol, 
                 task_repo: TaskRepositoryProtocol, 
                 task_history_repo: TaskHistoryRepositoryProtocol,
                 skill_repo: SkillRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol) -> None:
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.task_history_repo = task_history_repo
        self.skill_repo = skill_repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str) -> StatsOverviewDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        total_completed = await self.task_history_repo.get_amount_of_total_completed_tasks(user_id)
        completed_today = await self.task_history_repo.get_amount_of_today_completed_tasks(user_id)
        completed_this_week = await self.task_history_repo.get_amount_of_this_week_completed_tasks(user_id)
        overdue_count = await self.task_repo.get_amount_of_overdue_tasks(user_id)
        skills = await self.skill_repo.get_skills_by_lvl_desc_order(user_id)
        dto = StatsMapper.to_dto(
            user=user, 
            total_completed=total_completed, 
            completed_today=completed_today, 
            completed_this_week=completed_this_week, 
            overdue_count=overdue_count, 
            skills=skills)
        return dto