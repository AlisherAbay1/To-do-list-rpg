from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserRankNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRankRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.mappers import UserRankMapper
from uuid import UUID
from todo_rpg.application.dto import UserRankUpdateDTO
from todo_rpg.application.dto.sentinel_types import Unset


class UpdateCurrentUserRankInteractor:
    def __init__(
        self,
        repo: UserRankRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, user_rank_id: UUID, session_token: str, dto: UserRankUpdateDTO
    ):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user_rank = await self.repo.get_rank_by_id(user_rank_id)
        if user_rank is None:
            raise UserRankNotFoundError()
        if user_rank.user_id != user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset) and dto.title is not None:
            user_rank.title = dto.title

        output_dto = UserRankMapper.to_dto(user_rank)

        await self.uow.commit()

        return output_dto
