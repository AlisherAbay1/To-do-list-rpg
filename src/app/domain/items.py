from datetime import datetime
from typing import Optional
from uuid import UUID
from dataclasses import dataclass, field
from uuid6 import uuid7
from src.app.domain.skills import SkillDomain

@dataclass(kw_only=True)
class ItemDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str
    description: Optional[str] = None
    deleted: bool = False
    deleted_at: Optional[datetime] = None

    skills: list[SkillDomain] = field(init=False, default_factory=list)