from typing import Any

from app.repositories.interfaces import SkillRepositoryProtocol, RedisRepositoryProtocol, TransactionProtocol
from app.schemas import SkillCreateDTO, SkillDTO
from app.models import Skill
from app.exceptions import SkillNotFoundError, SessionNotFoundError
from uuid import UUID
from uuid_utils import uuid7
from datetime import datetime, timezone

class GetAllSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        skills = await self.repo.get_all_skills(limit, offset)
        return skills

class GetCurrentUserSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skills = await self.repo.get_skills_by_user_id(UUID(user_id), limit, offset)
        return skills

class CreateCurrentUserSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: SkillCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        skill_id = uuid7()
        user = Skill(
            id=skill_id,
            user_id=user_id, 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        )
        self.repo.save(user)
        await self.transaction.commit()
        return SkillDTO(
            id=UUID(str(skill_id)),
            user_id=UUID(user_id), 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        ) 

class GetSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        return skill

class DeleteSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        skill.deleted = True
        skill.deleted_at = datetime.now(tz=timezone.utc)
        await self.transaction.commit()

class ClearExpiredSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self) -> Any:
        await self.repo.delete_all_skills_deleted_more_than_year()
        await self.transaction.commit()