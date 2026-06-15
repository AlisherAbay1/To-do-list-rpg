from todo_rpg.application.interfaces.repositories_interfaces import (
    ShopRepositoryProtocol,
    InventoryRepositoryProtocol,
    ItemRepositoryProtocol,
    UserRepositoryProtocol,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from uuid import UUID
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ShopListingNotFoundError,
    AccessDeniedError,
    UserNotFoundError,
    ItemNotFoundError,
    UserBalanceNotEnoughError,
    UserDoesntFitSkillRequirementsError,
    ShopListingAmountIsZeroError,
)
from todo_rpg.domain import Inventory, ShopTransaction
from todo_rpg.application.mappers import ExtendedShopMapper
from todo_rpg.application.dto import ShopListingShortWithShortInventoryItemDTO


class BuyCurrentUserShopListingInteractor:
    def __init__(
        self,
        shop_repo: ShopRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
        item_repo: ItemRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.shop_repo = shop_repo
        self.inventory_repo = inventory_repo
        self.item_repo = item_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, session_token: str, shop_listing_id: UUID
    ) -> ShopListingShortWithShortInventoryItemDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        shop_listing = await self.shop_repo.get_shop_listing_by_id(shop_listing_id)
        if shop_listing is None:
            raise ShopListingNotFoundError()
        if shop_listing.user_id != user_id:
            raise AccessDeniedError()

        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()

        item = await self.item_repo.get_item_by_id(shop_listing.item_id)
        if item is None:
            raise ItemNotFoundError()

        if user.gold < shop_listing.price:
            raise UserBalanceNotEnoughError()
        if not item.does_fit_requirements():
            raise UserDoesntFitSkillRequirementsError()
        if shop_listing.quantity == 0:
            raise ShopListingAmountIsZeroError()

        user.gold -= shop_listing.price
        shop_listing.quantity -= 1

        inventory = await self.inventory_repo.get_inventory_item_by_item_id(
            shop_listing.item_id, user_id
        )

        if inventory is None:
            inventory = Inventory(
                user_id=user_id, item_id=shop_listing.item_id, quantity=1
            )

            await self.uow.add(inventory)
        else:
            inventory.quantity += 1

        shop_transaction = ShopTransaction(
            user_id=user_id,
            shop_listing_id=shop_listing.id,
            item_id=item.id,
            item_title=item.title,
            price=shop_listing.price,
        )

        await self.uow.add(shop_transaction)

        dto = ExtendedShopMapper.to_shop_listing_with_short_inventory_item(
            shop_listing_domain=shop_listing,
            inventory_item_domain=inventory,
            balance=user.gold,
        )

        await self.uow.commit()

        return dto
