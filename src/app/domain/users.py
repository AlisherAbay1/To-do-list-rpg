from uuid import UUID
from typing import Optional
from src.app.application.dto.tasks import TaskReward

class UserDomain:
    def __init__(
        self, 
        id: UUID, 
        username: str,
        email: str,
        password: str,
        lvl: int,
        xp: int,
        is_admin: bool,
        current_rank_id: Optional[UUID],
        profile_picture: Optional[str],
        gold: int,
        timezone: str,
        language: str
    ) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.lvl = lvl
        self.xp = xp
        self.is_admin = is_admin
        self.current_rank_id = current_rank_id
        self.profile_picture = profile_picture
        self.gold = gold
        self.timezone = timezone
        self.language = language

    def apply_rewards(self, rewards: TaskReward):
        self.xp += rewards.xp
        self.lvl = self.xp // 1000
        self.gold += rewards.gold
