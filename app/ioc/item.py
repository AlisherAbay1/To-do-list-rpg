from dishka import Provider, provide, Scope
from app.repositories.interfaces import ItemRepositoryProtocol
from app.repositories.items import ItemRepository
from app.services.interactors import GetAllItemsInteractor, GetCurrentUserItemsInteractor, CreateCurrentUserItemInteractor, \
                                    GetItemInteractor, DeleteItemInteractor


class ItemProvider(Provider):
    scope = Scope.REQUEST
    item_repository = provide(ItemRepository, provides=ItemRepositoryProtocol)
    get_all_items = provide(GetAllItemsInteractor)
    get_current_user_items = provide(GetCurrentUserItemsInteractor)
    get_item = provide(GetItemInteractor)
    create_item = provide(CreateCurrentUserItemInteractor)
    delete_item = provide(DeleteItemInteractor)