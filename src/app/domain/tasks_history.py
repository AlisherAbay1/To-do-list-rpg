from dataclasses import dataclass, field
from uuid import UUID
from uuid6 import uuid7
from datetime import datetime, timezone
from src.app.domain.skills import SkillDomain
from src.app.domain.items import ItemDomain

@dataclass(kw_only=True)
class TaskHistoryDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    task_id: UUID
    title: str
    completed_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    xp_earned: int
    gold_earned: int

    skills: list[SkillDomain] = field(init=False, default_factory=list)
    items: list[ItemDomain] = field(init=False, default_factory=list)