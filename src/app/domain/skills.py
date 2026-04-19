from src.app.application.dto.tasks import TaskReward
from uuid import UUID
from typing import Optional
from datetime import datetime

class SkillDomain:
    def __init__(self, 
                 id: UUID,
                 user_id: UUID,
                 title: str,
                 description: Optional[str],
                 ico: Optional[str],
                 lvl: int,
                 xp: int,
                 deleted: bool,
                 deleted_at: Optional[datetime]):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.ico = ico
        self.lvl = lvl
        self.xp = xp
        self.deleted = deleted
        self.deleted_at = deleted_at

    def apply_reward(self, xp: int):
        self.xp += xp
        self.lvl = self.xp // 1000