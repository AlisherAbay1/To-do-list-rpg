from src.app.application.dto.tasks import TaskReward
from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class SkillDomain:
    id: UUID
    user_id: UUID
    title: str
    lvl: int
    xp: int
    deleted: bool
    description: Optional[str]
    ico: Optional[str]
    deleted_at: Optional[datetime]

    def apply_reward(self, xp: int):
        self.xp += xp
        self.lvl = self.xp // 1000