from dataclasses import dataclass
from todo_rpg.application.dto.common import UserStatsDTO, TaskStatsDTO, SkillShortDTO


@dataclass
class StatsOverviewDTO:
    user: UserStatsDTO
    tasks: TaskStatsDTO
    skills: list[SkillShortDTO]
