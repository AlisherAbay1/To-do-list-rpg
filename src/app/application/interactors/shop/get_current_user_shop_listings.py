from src.app.application.interfaces.repositories_interfaces import (
    ShopRepositoryProtocol,
)
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.mappers import ShopMapper
from src.app.application.dto import ShopListingShortDTO
from src.app.application.exceptions import SessionNotFoundError


class GetCurrentUserShopListingsInteractor:
    def __init__(
        self, repo: ShopRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[ShopListingShortDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_listings = await self.repo.get_shop_listings_by_user_id(
            user_id, limit, offset
        )
        dtos = ShopMapper.to_short_list_dto(shop_listings)
        return dtos
