from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol

class GetAllSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        skills = await self.repo.get_all_skills(limit, offset)
        return skills