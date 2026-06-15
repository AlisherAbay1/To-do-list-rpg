from todo_rpg.application.exceptions import SkillNotFoundError
from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    UserRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO
from uuid import UUID
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetSkillInteractor:
    def __init__(
        self,
        skill_repo: SkillRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.skill_repo = skill_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, skill_id: UUID) -> SkillDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()
        skill = await self.skill_repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        dto = SkillMapper.to_dto(skill)
        return dto
