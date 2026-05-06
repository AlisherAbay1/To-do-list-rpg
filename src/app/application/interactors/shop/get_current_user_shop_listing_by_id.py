from src.app.application.interfaces.repositories_interfaces import ShopRepositoryProtocol, ItemRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.mappers import ExtendedShopMapper
from src.app.application.dto import ShopListingShortWithFtRequiremenetsDTO
from src.app.application.exceptions import (SessionNotFoundError, ShopListingNotFoundError, 
                                            AccessDeniedError, ItemNotFoundError)
from uuid import UUID

class GetCurrentUserShopListingByIdInteractor:
    def __init__(self, 
                 shop_repo: ShopRepositoryProtocol, 
                 item_repo: ItemRepositoryProtocol,
                 cash_repo: RedisRepositoryProtocol) -> None:
        self.shop_repo = shop_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, shop_listing_id: UUID) -> ShopListingShortWithFtRequiremenetsDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_listing = await self.shop_repo.get_shop_listings_by_id(shop_listing_id)
        if shop_listing is None:
            raise ShopListingNotFoundError()
        if shop_listing.user_id != user_id:
            raise AccessDeniedError()
        item = await self.item_repo.get_item_by_id_with_requirements_contains_skill(shop_listing.item_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ExtendedShopMapper.to_shop_listing_with_fit_requirement(shop_listing, item) 
        return dto