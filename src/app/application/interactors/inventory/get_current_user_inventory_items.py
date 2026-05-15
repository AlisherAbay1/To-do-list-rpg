from src.app.application.interfaces.repositories_interfaces import (
    InventoryRepositoryProtocol,
)
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.mappers import InventoryMapper
from src.app.application.dto import InventoryShortDTO
from src.app.application.exceptions import SessionNotFoundError


class GetCurrentUserInventoryItemsInteractor:
    def __init__(
        self, repo: InventoryRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[InventoryShortDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        inventory_items = await self.repo.get_inventory_items_by_user_id(
            user_id, limit, offset
        )
        dtos = InventoryMapper.to_short_list_dto(inventory_items)
        return dtos
