from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    UserRankNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.interfaces import (
    RedisRepositoryProtocol,
    UserRepositoryProtocol,
    UserRankRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from uuid import UUID


class ChangeCurrentUserRankInteractor:
    def __init__(
        self,
        user_repo: UserRepositoryProtocol,
        user_rank_repo: UserRankRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.user_repo = user_repo
        self.user_rank_repo = user_rank_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, rank_id: UUID):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        user = await self.user_repo.get_user(user_id)
        if not user:
            raise UserNotFoundError()

        user_rank = await self.user_rank_repo.get_rank_by_id(rank_id)
        if user_rank is None:
            raise UserRankNotFoundError()
        if user_rank.user_id != user_id:
            raise AccessDeniedError()

        user.current_rank_id = rank_id

        rank_title = user_rank.title

        await self.uow.commit()
        return rank_title
