from dishka import Provider, provide, Scope
from src.app.infrastructure.database.repositories.task_categories import TaskCategoriesRepository
from src.app.application.interfaces.repositories_interfaces import TaskCategoriesRepositoryProtocol
from src.app.application.interactors.task_categories import GetAllTaskCategories, GetCurrentUserTaskCategories, CreateCurrentUserTaskCategory, \
                                                            UpdateCurrentUserTaskCategory

class TaskCategoriesProvider(Provider):
    scope = Scope.REQUEST
    task_categories_repository = provide(TaskCategoriesRepository, provides=TaskCategoriesRepositoryProtocol)
    get_all_task_categories = provide(GetAllTaskCategories)
    get_current_user_task_categories = provide(GetCurrentUserTaskCategories)
    create_current_user_task_category = provide(CreateCurrentUserTaskCategory)
    update_current_user_task_category = provide(UpdateCurrentUserTaskCategory)