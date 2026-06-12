from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    AccessDeniedError,
    UserRankNotFoundError,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRankRepositoryProtocol,
)
from todo_rpg.application.mappers import UserRankMapper
from uuid import UUID


class GetCurrentUserRankInteractor:
    def __init__(
        self, repo: UserRankRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, user_rank_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user_rank = await self.repo.get_rank_by_id(user_rank_id)
        if user_rank is None:
            raise UserRankNotFoundError()
        if user_rank.user_id != user_id:
            raise AccessDeniedError()
        dto = UserRankMapper.to_dto(user_rank)
        return dto
