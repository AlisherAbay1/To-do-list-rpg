from dishka import Provider, provide, Scope
from todo_rpg.application.interfaces.repositories_interfaces import (
    InventoryRepositoryProtocol,
)
from todo_rpg.infrastructure.database.repositories import InventoryRepository
from todo_rpg.application.interactors import (
    GetCurrentUserInventoryItemByIdInteractor,
    GetCurrentUserInventoryItemsInteractor,
    DeleteCurrentUserInventoryItemInteractor,
    UseCurrentUserInventoryItemInteractor,
)


class InventoryProvider(Provider):
    scope = Scope.REQUEST
    inventory_repository = provide(
        InventoryRepository, provides=InventoryRepositoryProtocol
    )
    delete_current_user_inventory_item = provide(
        DeleteCurrentUserInventoryItemInteractor
    )
    get_current_user_inventory_item_by_id = provide(
        GetCurrentUserInventoryItemByIdInteractor
    )
    get_current_user_inventory_items = provide(GetCurrentUserInventoryItemsInteractor)
    use_current_user_inventory_item = provide(UseCurrentUserInventoryItemInteractor)
