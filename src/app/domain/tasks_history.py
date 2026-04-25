from dataclasses import dataclass, field
from uuid import UUID
from uuid6 import uuid7
from datetime import datetime, timezone

@dataclass(kw_only=True)
class TaskHistoryDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    task_id: UUID
    title: str
    completed_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    xp_earned: int
    gold_earned: int