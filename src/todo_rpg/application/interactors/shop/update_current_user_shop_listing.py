from todo_rpg.application.interfaces.repositories_interfaces import (
    ShopRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.mappers import ShopMapper
from todo_rpg.application.dto import ShopListingShortDTO, ShopListingUpdateDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ShopListingNotFoundError,
    AccessDeniedError,
)
from todo_rpg.application.dto.sentinel_types import Unset
from uuid import UUID


class UpdateCurrentUserShopListingInteractor:
    def __init__(
        self,
        repo: ShopRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, shop_listing_id: UUID, session_token: str, dto: ShopListingUpdateDTO
    ) -> ShopListingShortDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_listing = await self.repo.get_shop_listing_by_id(shop_listing_id)
        if shop_listing is None:
            raise ShopListingNotFoundError()
        if shop_listing.user_id != user_id:
            raise AccessDeniedError()

        if not isinstance(dto.price, Unset) and dto.price is not None:
            shop_listing.price = dto.price
        if not isinstance(dto.quantity, Unset) and dto.quantity is not None:
            shop_listing.quantity = dto.quantity

        output_dto = ShopMapper.to_short_dto(shop_listing)

        await self.uow.commit()

        return output_dto
