from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    UoWProtocol,
    SessionRepositoryProtocol,
)
from todo_rpg.application.dto import SkillUpdateDTO, SkillDTO
from todo_rpg.application.mappers import SkillMapper
from uuid import UUID
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    SkillNotFoundError,
    AccessDeniedError,
)
from todo_rpg.domain.sentinel_types import Unset


class UpdateCurrentUserSkillInteractor:
    def __init__(
        self,
        repo: SkillRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(
        self, skill_id: UUID, dto: SkillUpdateDTO, session_token: str
    ) -> SkillDTO:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        if user_id != skill.user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset) and dto.title is not None:
            skill.title = dto.title
        if not isinstance(dto.description, Unset):
            skill.description = dto.description
        if not isinstance(dto.icon, Unset):
            skill.icon = dto.icon
        if not isinstance(dto.xp, Unset) and dto.xp is not None:
            skill.xp = dto.xp
        if not isinstance(dto.lvl, Unset) and dto.lvl is not None:
            skill.lvl = dto.lvl

        output_dto = SkillMapper.to_dto(skill)
        await self.uow.commit()
        return output_dto
