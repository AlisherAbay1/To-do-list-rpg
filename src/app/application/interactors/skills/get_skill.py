from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol
from src.app.application.exceptions import SkillNotFoundError

class GetSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        return skill