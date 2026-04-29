from dishka import Provider, provide, Scope
from src.app.infrastructure.database.repositories.task_categories import TaskCategoriesRepository
from src.app.application.interfaces.repositories_interfaces import TaskCategoriesRepositoryProtocol
from src.app.application.interactors.task_categories import GetAllTaskCategories

class TaskCategoriesProvider(Provider):
    scope = Scope.REQUEST
    task_categories_repository = provide(TaskCategoriesRepository, provides=TaskCategoriesRepositoryProtocol)
    get_all_task_categories = provide(GetAllTaskCategories)