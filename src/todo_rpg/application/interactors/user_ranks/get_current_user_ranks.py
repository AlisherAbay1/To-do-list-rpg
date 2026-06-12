from todo_rpg.application.interfaces import (
    RedisRepositoryProtocol,
    UserRankRepositoryProtocol,
)
from todo_rpg.application.mappers import UserRankMapper
from todo_rpg.application.exceptions import SessionNotFoundError


class GetCurrentUserRanksInteractor:
    def __init__(
        self, repo: UserRankRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user_ranks = await self.repo.get_ranks_by_user_id(user_id, limit, offset)
        return UserRankMapper.to_list_dto(user_ranks)
