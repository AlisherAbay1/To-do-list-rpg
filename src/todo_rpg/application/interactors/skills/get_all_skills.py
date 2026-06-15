from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    RedisRepositoryProtocol,
    UserRepositoryProtocol,
)
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetAllSkillsInteractor:
    def __init__(
        self,
        skill_repo: SkillRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.skill_repo = skill_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[SkillDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()
        skills = await self.skill_repo.get_all_skills(limit, offset)
        dtos = SkillMapper.to_list_dto(skills)
        return dtos
