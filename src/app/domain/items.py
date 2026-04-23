from datetime import datetime
from typing import Optional
from uuid import UUID
from dataclasses import dataclass

@dataclass
class ItemDomain:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    deleted: bool
    deleted_at: Optional[datetime]