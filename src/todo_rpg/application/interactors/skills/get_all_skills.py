from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO


class GetAllSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int) -> list[SkillDTO]:
        skills = await self.repo.get_all_skills(limit, offset)
        dtos = SkillMapper.to_list_dto(skills)
        return dtos
