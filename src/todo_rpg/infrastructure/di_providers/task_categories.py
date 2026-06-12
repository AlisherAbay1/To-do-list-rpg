from dishka import Provider, provide, Scope
from todo_rpg.infrastructure.database.repositories.task_categories import (
    TaskCategoriesRepository,
)
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.interactors.task_categories import (
    GetAllTaskCategories,
    GetCurrentUserTaskCategories,
    CreateCurrentUserTaskCategory,
    UpdateCurrentUserTaskCategory,
    GetCurrentUserTaskCategoryById,
    DeleteCurrentUserTaskCategoryById,
)


class TaskCategoriesProvider(Provider):
    scope = Scope.REQUEST
    task_categories_repository = provide(
        TaskCategoriesRepository, provides=TaskCategoriesRepositoryProtocol
    )
    get_all_task_categories = provide(GetAllTaskCategories)
    get_current_user_task_categories = provide(GetCurrentUserTaskCategories)
    create_current_user_task_category = provide(CreateCurrentUserTaskCategory)
    update_current_user_task_category = provide(UpdateCurrentUserTaskCategory)
    get_current_user_task_category_by_id = provide(GetCurrentUserTaskCategoryById)
    delete_current_user_task_category_by_id = provide(DeleteCurrentUserTaskCategoryById)
