from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ItemNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers import ItemExtendedMapper
from uuid import UUID
from todo_rpg.application.dto import ItemWithRequirementsDTO


class GetCurrentUserItemInteractor:
    def __init__(
        self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, item_id: UUID, session_token: str
    ) -> ItemWithRequirementsDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()
        dto = ItemExtendedMapper.to_dto_with_requirements(item)
        return dto
