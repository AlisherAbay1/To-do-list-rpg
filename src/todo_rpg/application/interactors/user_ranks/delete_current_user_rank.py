from uuid import UUID

from todo_rpg.application.interfaces import (
    UserRankRepositoryProtocol,
    SessionRepositoryProtocol,
    UoWProtocol,
)
from todo_rpg.application.exceptions import (
    AccessDeniedError,
    SessionNotFoundError,
    UserRankNotFoundError,
)


class DeleteCurrentUserRankInteractor:
    def __init__(
        self,
        repo: UserRankRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, session_token: str, user_rank_id: UUID) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user_rank = await self.repo.get_rank_by_id(user_rank_id)
        if user_rank is None:
            raise UserRankNotFoundError()
        if user_rank.user_id != user_id:
            raise AccessDeniedError()

        await self.uow.delete(user_rank)
        await self.uow.commit()
