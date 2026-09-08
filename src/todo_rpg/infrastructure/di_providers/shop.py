from dishka import Provider, provide, Scope
from todo_rpg.application.interfaces import (
    ShopRepositoryProtocol,
    ShopTransactionRepositoryProtocol,
)
from todo_rpg.infrastructure.database.repositories import (
    ShopRepository,
    ShopTransactionRepository,
)
from todo_rpg.application.interactors import (
    GetCurrentUserShopListingsInteractor,
    CreateCurrentUserShopListingInteractor,
    UpdateCurrentUserShopListingInteractor,
    DeleteCurrentUserShopListingInteractor,
    GetCurrentUserShopListingByIdInteractor,
    BuyCurrentUserShopListingInteractor,
    GetShopTransactionsInteractor,
    CancelTransactionInteractor,
)


class ShopProvider(Provider):
    scope = Scope.REQUEST
    shop_repository = provide(ShopRepository, provides=ShopRepositoryProtocol)
    shop_transaction_repository = provide(
        ShopTransactionRepository, provides=ShopTransactionRepositoryProtocol
    )
    get_current_user_shop_listings = provide(GetCurrentUserShopListingsInteractor)
    create_current_user_shop_listing = provide(CreateCurrentUserShopListingInteractor)
    update_current_user_shop_listing = provide(UpdateCurrentUserShopListingInteractor)
    delete_current_user_shop_listing = provide(DeleteCurrentUserShopListingInteractor)
    get_current_user_shop_listing_by_id = provide(
        GetCurrentUserShopListingByIdInteractor
    )
    buy_current_user_shop_listing = provide(BuyCurrentUserShopListingInteractor)
    get_shop_transactions = provide(GetShopTransactionsInteractor)
    cancel_transaction = provide(CancelTransactionInteractor)
