from app.repositories.interfaces import SkillRepositoryProtocol, RedisRepositoryProtocol
from app.schemas import SkillCreateOrUpdateDTO
from app.models import Skill
from app.exceptions import SkillNotFoundError

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

    async def __call__(self, session_id: str, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        skills = await self.repo.get_skills_by_user_id(user_id, limit, offset)
        return skills

class CreateCurrentUserSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id: str, dto: SkillCreateOrUpdateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        user = Skill(
            user_id=user_id, 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        )
        self.repo.save(user)
        return dto

class GetSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        return skill

class DeleteSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        await self.repo.delete(skill)
        return skill
