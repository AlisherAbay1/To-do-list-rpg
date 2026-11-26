from todo_rpg.application.interfaces import (
    ShopRepositoryProtocol,
    SessionRepositoryProtocol,
)
from todo_rpg.application.mappers import ShopMapper
from todo_rpg.application.dto import ShopListingShortDTO
from todo_rpg.application.exceptions import SessionNotFoundError


class GetCurrentUserShopListingsInteractor:
    def __init__(
        self, repo: ShopRepositoryProtocol, session_repo: SessionRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[ShopListingShortDTO]:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        shop_listings = await self.repo.get_shop_listings_by_user_id(
            user_id, limit, offset
        )

        dtos = ShopMapper.to_short_list_dto(shop_listings)
        return dtos
