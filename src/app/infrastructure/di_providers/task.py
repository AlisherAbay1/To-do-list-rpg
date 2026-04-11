from dishka import Provider, provide, Scope
from src.app.infrastructure.database.repositories import TaskRepository, TaskHistoryRepository
from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol, TaskHistoryRepositoryProtocol
from src.app.application.interactors import GetAllTasksInteractor, CreateCurrentUserTaskInteractor, GetCurentUserTasksInteractor, \
                                     GetTaskInteractor, DeleteTaskInteractor, CompleteTaskInteractor, \
                                     UpdateTaskInteractor, UncompleteTaskInteractor

class TaskProvider(Provider):
    scope = Scope.REQUEST
    task_repository = provide(TaskRepository, provides=TaskRepositoryProtocol)
    task_history_repository = provide(TaskHistoryRepository, provides=TaskHistoryRepositoryProtocol)
    get_all_tasks = provide(GetAllTasksInteractor)
    get_current_user_tasks = provide(GetCurentUserTasksInteractor)
    get_task = provide(GetTaskInteractor)
    create_task = provide(CreateCurrentUserTaskInteractor)
    update_task = provide(UpdateTaskInteractor)
    delete_task = provide(DeleteTaskInteractor)
    complete_task = provide(CompleteTaskInteractor)
    uncomplete_task = provide(UncompleteTaskInteractor)