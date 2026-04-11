from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass(slots=True)
class ItemDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    deleted: bool = False
    deleted_at: Optional[datetime] = None

@dataclass(slots=True)
class ItemUpdateDTO:
    title: Optional[str]
    description: Optional[str]


@dataclass(slots=True)
class ItemCreateDTO:
    title: str
    description: Optional[str]
