from app.models.skills import Skill
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Sequence
from uuid import UUID

class SkillRepository:
    __slots__ = ("_session")
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_skills(self, limit: int, offset: int) -> Sequence[Skill]:
        skills = select(Skill).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_skills_by_user_id(self, user_id: UUID, limit: int, offset: int) -> Sequence[Skill]:
        skills = select(Skill).where(Skill.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_skill_by_id(self, skill_id: UUID) -> Optional[Skill]:
        skill = select(Skill).where(Skill.id == skill_id)
        result = await self._session.scalar(skill)
        return result
    
    def save(self, skill: Skill):
        self._session.add(skill)

    async def delete(self, skill: Skill):
        await self._session.delete(skill)