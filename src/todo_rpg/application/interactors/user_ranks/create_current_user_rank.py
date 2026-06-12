from todo_rpg.application.dto import UserRankCreateDTO
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRankRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.domain import UserRank
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.mappers.common import UserRankMapper


class CreateCurrentUserRankInteractor:
    def __init__(
        self,
        repo: UserRankRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, dto: UserRankCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user_rank = UserRank(user_id=user_id, title=dto.title)
        output_dto = UserRankMapper.to_dto(user_rank)
        await self.uow.add(user_rank)
        await self.uow.commit()
        return output_dto
