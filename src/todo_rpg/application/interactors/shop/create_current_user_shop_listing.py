from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.interfaces import (
    ShopRepositoryProtocol,
    ItemRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers import ShopMapper
from todo_rpg.application.dto import ShopListingShortDTO, ShopListingCreateDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ShopListingAlreadyExistsError,
    ItemNotFoundError,
    AccessDeniedError,
)
from todo_rpg.domain import Shop


class CreateCurrentUserShopListingInteractor:
    def __init__(
        self,
        shop_repo: ShopRepositoryProtocol,
        item_repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.shop_repo = shop_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, session_token: str, dto: ShopListingCreateDTO
    ) -> ShopListingShortDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        item = await self.item_repo.get_item_by_id(dto.item_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()

        possible_shop_listing = await self.shop_repo.get_shop_listing_by_item_id(
            dto.item_id
        )
        if possible_shop_listing is not None:
            raise ShopListingAlreadyExistsError()

        shop_listing = Shop(
            user_id=user_id, item_id=dto.item_id, price=dto.price, quantity=dto.quantity
        )
        await self.uow.add(shop_listing)
        output_dto = ShopMapper.to_short_dto(shop_listing)
        await self.uow.commit()
        return output_dto
