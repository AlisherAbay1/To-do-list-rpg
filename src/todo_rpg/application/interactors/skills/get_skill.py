from todo_rpg.application.exceptions import SkillNotFoundError
from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO


class GetSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, skill_id) -> SkillDTO:
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        dto = SkillMapper.to_dto(skill)
        return dto
