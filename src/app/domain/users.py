from uuid import UUID
from typing import Optional
from src.app.application.dto.tasks import TaskReward
from dataclasses import dataclass, field
from uuid6 import uuid7

@dataclass(kw_only=True)
class UserDomain:
    id: UUID = field(default_factory=uuid7)
    username: str
    email: str
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID] = None
    profile_picture: Optional[str] = None
    gold: int = 0
    language: str = "eng"
    timezone: str = "UTC"

    def apply_rewards(self, rewards: TaskReward):
        self.xp += rewards.xp
        self.lvl = 1 + self.xp // 1000
        self.gold += rewards.gold
