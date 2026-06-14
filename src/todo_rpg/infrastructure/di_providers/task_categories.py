from dishka import Provider, provide, Scope
from todo_rpg.infrastructure.database.repositories.task_categories import (
    TaskCategoriesRepository,
)
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.interactors.task_categories import (
    GetAllTaskCategoriesInteractor,
    GetCurrentUserTaskCategoriesInteractor,
    CreateCurrentUserTaskCategoryInteractor,
    UpdateCurrentUserTaskCategoryInteractor,
    GetCurrentUserTaskCategoryByIdInteractor,
    DeleteCurrentUserTaskCategoryByIdInteractor,
)


class TaskCategoriesProvider(Provider):
    scope = Scope.REQUEST
    task_categories_repository = provide(
        TaskCategoriesRepository, provides=TaskCategoriesRepositoryProtocol
    )
    get_all_task_categories = provide(GetAllTaskCategoriesInteractor)
    get_current_user_task_categories = provide(GetCurrentUserTaskCategoriesInteractor)
    create_current_user_task_category = provide(CreateCurrentUserTaskCategoryInteractor)
    update_current_user_task_category = provide(UpdateCurrentUserTaskCategoryInteractor)
    get_current_user_task_category_by_id = provide(
        GetCurrentUserTaskCategoryByIdInteractor
    )
    delete_current_user_task_category_by_id = provide(
        DeleteCurrentUserTaskCategoryByIdInteractor
    )
