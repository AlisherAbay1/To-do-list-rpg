from dishka import Provider, provide, Scope
from src.app.application.interfaces.repositories_interfaces import ShopRepositoryProtocol
from src.app.infrastructure.database.repositories import ShopRepository
from src.app.application.interactors import (
    GetCurrentUserShopListingsInteractor, CreateCurrentUserShopListing
)

class ShopProvider(Provider):
    scope = Scope.REQUEST
    shop_repository = provide(ShopRepository, provides=ShopRepositoryProtocol)
    get_current_user_shop_listings = provide(GetCurrentUserShopListingsInteractor)
    create_current_user_shop_listing = provide(CreateCurrentUserShopListing)