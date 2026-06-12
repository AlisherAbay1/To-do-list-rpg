from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class SkillSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int
    deleted: bool
    deleted_at: Optional[datetime]


class SkillSchemaCreate(BaseModel):
    title: str
    description: Optional[str]
    ico: Optional[str] = None
    lvl: int = 1
    xp: int = 0


class SkillSchemaUpdate(BaseModel):
    title: str | None = None
    description: Optional[str] = None
    ico: Optional[str] = None
    lvl: int | None = None
    xp: int | None = None


class SkillShortSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    ico: Optional[str]
    lvl: int
    xp: int


class SkillRequirementsSchema(BaseModel):
    skill: SkillShortSchema
    required_lvl: int


class SkillRequirementsWithFitRequiremenetSchema(BaseModel):
    skill: SkillShortSchema
    required_lvl: int
    fit_requirement: bool
