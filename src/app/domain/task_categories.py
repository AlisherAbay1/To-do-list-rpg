from dataclasses import dataclass, field
from uuid import UUID
from uuid6 import uuid7

@dataclass(kw_only=True)
class TaskCategoryDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str
    color: str