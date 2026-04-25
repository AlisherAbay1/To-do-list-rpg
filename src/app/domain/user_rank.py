from dataclasses import dataclass, field
from uuid6 import uuid7
from uuid import UUID

@dataclass(kw_only=True)
class UserRankDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str