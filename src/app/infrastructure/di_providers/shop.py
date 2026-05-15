from dishka import Provider, provide, Scope
from src.app.application.interfaces.repositories_interfaces import (
    ShopRepositoryProtocol,
)
from src.app.infrastructure.database.repositories import ShopRepository
from src.app.application.interactors import (
    GetCurrentUserShopListingsInteractor,
    CreateCurrentUserShopListingInteractor,
    UpdateCurrentUserShopListingInteractor,
    DeleteCurrentUserShopListingInteractor,
    GetCurrentUserShopListingByIdInteractor,
    BuyCurrentUserShopListingInteractor,
)


class ShopProvider(Provider):
    scope = Scope.REQUEST
    shop_repository = provide(ShopRepository, provides=ShopRepositoryProtocol)
    get_current_user_shop_listings = provide(GetCurrentUserShopListingsInteractor)
    create_current_user_shop_listing = provide(CreateCurrentUserShopListingInteractor)
    update_current_user_shop_listing = provide(UpdateCurrentUserShopListingInteractor)
    delete_current_user_shop_listing = provide(DeleteCurrentUserShopListingInteractor)
    get_current_user_shop_listing_by_id = provide(
        GetCurrentUserShopListingByIdInteractor
    )
    buy_current_user_shop_listing = provide(BuyCurrentUserShopListingInteractor)
