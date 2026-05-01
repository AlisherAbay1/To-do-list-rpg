from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass(slots=True)
class SkillDTO:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]

@dataclass(slots=True)
class SkillCreateDTO:
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int

@dataclass(slots=True)
class SkillUpdateDTO:
    title: Optional[str]
    description: Optional[str]
    ico: Optional[str]
    lvl: Optional[int]
    xp: Optional[int]