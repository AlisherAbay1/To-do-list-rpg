from datetime import datetime
from typing import Optional
from uuid import UUID
from dataclasses import dataclass, field
from uuid6 import uuid7

@dataclass(kw_only=True)
class ItemDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str
    description: Optional[str] = None
    deleted: bool = False
    deleted_at: Optional[datetime]