from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.app.application.dto.sentinel_types import UNSET, Unset

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
    title: str | Unset = UNSET
    description: Optional[str] | Unset = UNSET
    ico: Optional[str] | Unset = UNSET
    lvl: int | Unset = UNSET
    xp: int | Unset = UNSET

@dataclass(slots=True)
class SkillShortDTO:
    id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int

@dataclass(slots=True)
class SkillRequirementsDTO:
    skill: SkillShortDTO
    required_lvl: int

@dataclass(slots=True)
class SkillRequirementsWithFitRequiremenetDTO:
    skill: SkillShortDTO
    required_lvl: int
    fit_requirement: bool