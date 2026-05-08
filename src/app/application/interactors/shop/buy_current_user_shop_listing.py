from src.app.application.interfaces.repositories_interfaces import (ShopRepositoryProtocol, 
                                                                    InventoryRepositoryProtocol, 
                                                                    ItemRepositoryProtocol, 
                                                                    UserRepositoryProtocol)
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from uuid import UUID
from src.app.application.exceptions import (SessionNotFoundError, 
                                            ShopListingNotFoundError, 
                                            AccessDeniedError, 
                                            UserNotFoundError, 
                                            ItemNotFoundError, 
                                            UserBalanceNotEnoughError, 
                                            UserDoesntFitSkillRequirementsError)
from src.app.domain import Inventory
from src.app.application.mappers import ExtendedShopMapper
from src.app.application.dto import ShopListingShortWithShortInventoryItemDTO

class BuyCurrentUserShopListingInteractor:
    def __init__(self, 
                 shop_repo: ShopRepositoryProtocol,
                 inventory_repo: InventoryRepositoryProtocol, 
                 item_repo: ItemRepositoryProtocol, 
                 user_repo: UserRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.shop_repo = shop_repo
        self.inventory_repo = inventory_repo
        self.item_repo = item_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, shop_listing_id: UUID) -> ShopListingShortWithShortInventoryItemDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_listing = await self.shop_repo.get_shop_listing_by_id(shop_listing_id)
        if shop_listing is None:
            raise ShopListingNotFoundError()
        if shop_listing.user_id != user_id:
            raise AccessDeniedError()
        user = await self.user_repo.get_user(user_id)
        inventory = await self.inventory_repo.get_inventory_item_by_item_id(shop_listing.item_id, user_id)
        item = await self.item_repo.get_item_by_id_with_requirements_contains_skill(shop_listing.item_id, user_id)
        if user is None:
            raise UserNotFoundError()
        if item is None:
            raise ItemNotFoundError()
        
        if user.gold < shop_listing.price:
            raise UserBalanceNotEnoughError()
        if not item.does_fit_requirements():
            raise UserDoesntFitSkillRequirementsError()
        user.gold -= shop_listing.price
        shop_listing.quantity -= 1

        if inventory is None:
            inventory = Inventory(
                user_id=user_id, 
                item_id=shop_listing.item_id, 
                quantity=1
            )

            await self.transaction.save(inventory)
        else:
            inventory.quantity += 1

        dto = ExtendedShopMapper.to_shop_listing_with_short_inventory_item(
            shop_listing_domain=shop_listing, 
            inventory_item_domain=inventory, 
            balance=user.gold
        )

        if shop_listing.quantity == 0:
            await self.transaction.delete(shop_listing)

        await self.transaction.commit()

        return dto