from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.dto import SkillUpdateDTO, SkillDTO
from todo_rpg.application.mappers import SkillMapper
from uuid import UUID
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    SkillNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.dto.sentinel_types import Unset


class UpdateCurrentUserSkillById:
    def __init__(
        self,
        repo: SkillRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(
        self, skill_id: UUID, dto: SkillUpdateDTO, session_token: str
    ) -> SkillDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        if user_id != skill.user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset):
            skill.title = dto.title
        if not isinstance(dto.description, Unset):
            skill.description = dto.description
        if not isinstance(dto.ico, Unset):
            skill.ico = dto.ico
        if not isinstance(dto.xp, Unset):
            skill.xp = dto.xp
        if not isinstance(dto.lvl, Unset):
            skill.lvl = dto.lvl

        output_dto = SkillMapper.to_dto(skill)
        await self.transaction.commit()
        return output_dto
