from src.app.application.dto import (
    StatsOverviewDTO,
    UserStatsDTO,
    TaskStatsDTO,
    SkillShortDTO,
)
from src.app.domain import User, Skill
from typing import Optional, Sequence


class StatsMapper:
    @staticmethod
    def to_dto(
        user: User,
        total_completed: Optional[int],
        completed_today: Optional[int],
        completed_this_week: Optional[int],
        overdue_count: Optional[int],
        skills: Sequence[Skill],
    ) -> StatsOverviewDTO:

        dto = StatsOverviewDTO(
            user=UserStatsDTO(
                lvl=user.lvl,
                xp=user.xp,
                xp_to_next_level=user.calculate_xp_for_next_lvl(user.xp),
                gold=user.gold,
            ),
            tasks=TaskStatsDTO(
                total_completed=total_completed or 0,
                completed_today=completed_today or 0,
                completed_this_week=completed_this_week or 0,
                overdue_count=overdue_count or 0,
            ),
            skills=[
                SkillShortDTO(
                    id=skill.id,
                    title=skill.title,
                    description=skill.description,
                    ico=skill.ico,
                    lvl=skill.lvl,
                    xp=skill.xp,
                )
                for skill in skills
            ],
        )
        return dto
