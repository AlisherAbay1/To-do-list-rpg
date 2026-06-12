from dishka import Provider, provide, Scope
from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.infrastructure.database.repositories import ItemRepository
from todo_rpg.application.interactors import (
    GetAllItemsInteractor,
    GetCurrentUserItemsInteractor,
    CreateCurrentUserItemInteractor,
    GetItemInteractor,
    DeleteItemInteractor,
    GetCurrentUserItemInteractor,
    UpdateCurrentUserItemInteractor,
    DeleteCurrentUserItemInteractor,
    AddCurrentUserItemRequirementInteractor,
    DeleteCurrentUserSkillRequirementInteractor,
)


class ItemProvider(Provider):
    scope = Scope.REQUEST
    item_repository = provide(ItemRepository, provides=ItemRepositoryProtocol)
    get_all_items = provide(GetAllItemsInteractor)
    get_current_user_items = provide(GetCurrentUserItemsInteractor)
    get_item = provide(GetItemInteractor)
    create_item = provide(CreateCurrentUserItemInteractor)
    delete_item = provide(DeleteItemInteractor)
    get_current_user_item = provide(GetCurrentUserItemInteractor)
    update_current_user_item = provide(UpdateCurrentUserItemInteractor)
    delete_current_user_item = provide(DeleteCurrentUserItemInteractor)
    add_current_user_item_requirement = provide(AddCurrentUserItemRequirementInteractor)
    delete_current_user_skill_requirement = provide(
        DeleteCurrentUserSkillRequirementInteractor
    )
