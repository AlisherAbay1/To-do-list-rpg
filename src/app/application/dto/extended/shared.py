from dataclasses import dataclass
from src.app.application.dto.common import UserStatsDTO, TaskStatsDTO, SkillShortDTO

@dataclass 
class StatsOverviewDTO:
    user: UserStatsDTO
    tasks: TaskStatsDTO
    skills: list[SkillShortDTO]