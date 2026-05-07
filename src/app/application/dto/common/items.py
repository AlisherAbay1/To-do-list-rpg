from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.app.application.dto.sentinel_types import Unset, UNSET

@dataclass(slots=True)
class ItemDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    deleted: bool
    deleted_at: Optional[datetime]

@dataclass(slots=True)
class ItemCreateDTO:
    title: str
    description: Optional[str]

@dataclass(slots=True)
class ItemUpdateDTO:
    title: str | Unset = UNSET
    description: Optional[str] | Unset = UNSET