from src.app.application.interfaces.repositories_interfaces import \
    SkillRepositoryProtocol
from src.app.application.mappers.common import SkillMapper

class GetAllSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        skills = await self.repo.get_all_skills(limit, offset)
        dtos = SkillMapper.to_list_dto(skills)
        return dtos