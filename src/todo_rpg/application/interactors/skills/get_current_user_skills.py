from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers.common import SkillMapper
from todo_rpg.application.dto import SkillDTO


class GetCurrentUserSkillsInteractor:
    def __init__(
        self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[SkillDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skills = await self.repo.get_skills_by_user_id(user_id, limit, offset)
        dtos = SkillMapper.to_list_dto(skills)
        return dtos
