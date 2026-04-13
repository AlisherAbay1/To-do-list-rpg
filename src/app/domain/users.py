
from uuid import UUID
from typing import Optional


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
        gold: int
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

    def add_xp(self, xp: int):
        self.xp += xp
        self.lvl = self.xp // 1000

    def add_gold(self, gold: int):
        self.gold += gold