from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

@dataclass(kw_only=True)
class ItemHistoryDomain:
    user_id: UUID
    item_id: UUID
    title: str
    used_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))