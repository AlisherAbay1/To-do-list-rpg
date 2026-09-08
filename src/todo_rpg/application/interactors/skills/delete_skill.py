from uuid import UUID

from todo_rpg.application.exceptions import (
    SkillNotFoundError,
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.interfaces import (
    SkillRepositoryProtocol,
    RedisRepositoryProtocol,
    UserRepositoryProtocol,
    UoWProtocol,
)


class DeleteSkillInteractor:
    def __init__(
        self,
        skill_repo: SkillRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.skill_repo = skill_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, skill_id: UUID) -> None:
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
        skill.delete()
        await self.uow.commit()
