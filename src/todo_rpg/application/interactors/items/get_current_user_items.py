from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers.common import ItemMapper
from todo_rpg.application.dto import ItemDTO


class GetCurrentUserItemsInteractor:
    def __init__(
        self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int, get_deleted: bool
    ) -> list[ItemDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        items = await self.repo.get_items_by_user_id(
            user_id, limit, offset, get_deleted
        )
        dtos = ItemMapper.to_list_dto(items)
        return dtos
