from dishka import Provider, provide, Scope
from src.app.application.interfaces.repositories_interfaces import InventoryRepositoryProtocol
from src.app.infrastructure.database.repositories import InventoryRepository
from src.app.application.interactors import (
        GetCurrentUserInventoryItemByIdInteractor, 
        GetCurrentUserInventoryItemsInteractor, 
        DeleteCurrentUserInventoryItemInteractor
)

class InventoryProvider(Provider):
    scope = Scope.REQUEST
    inventory_repository = provide(InventoryRepository, provides=InventoryRepositoryProtocol)
    delete_current_user_inventory_item = provide(DeleteCurrentUserInventoryItemInteractor)
    get_current_user_inventory_item_by_id = provide(GetCurrentUserInventoryItemByIdInteractor)
    get_current_user_inventory_items = provide(GetCurrentUserInventoryItemsInteractor)