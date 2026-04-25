from src.app.application.dto.tasks import TaskReward
from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from uuid6 import uuid7

@dataclass(kw_only=True)
class SkillDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str
    description: Optional[str] = None
    ico: Optional[str] = None
    lvl: int = 1
    xp: int = 0
    deleted: bool = False
    deleted_at: Optional[datetime] = None

    def apply_reward(self, xp: int):
        self.xp += xp
        self.lvl = self.xp // 1000