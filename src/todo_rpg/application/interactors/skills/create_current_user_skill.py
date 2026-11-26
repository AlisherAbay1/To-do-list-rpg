from todo_rpg.application.dto.common.skills import SkillCreateDTO
from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    SessionRepositoryProtocol,
    UoWProtocol,
)
from todo_rpg.domain import Skill
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO


class CreateCurrentUserSkillInteractor:
    def __init__(
        self,
        repo: SkillRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, session_token: str, dto: SkillCreateDTO) -> SkillDTO:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = Skill(
            user_id=user_id,
            title=dto.title,
            description=dto.description,
            ico=dto.ico,
            lvl=dto.lvl,
            xp=dto.xp,
        )
        output_dto = SkillMapper.to_dto(skill)
        self.uow.add(skill)
        await self.uow.commit()
        return output_dto
