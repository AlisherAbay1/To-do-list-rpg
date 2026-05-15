from dishka import Provider, provide, Scope
from src.app.infrastructure.database.repositories import (
    TaskRepository,
    TaskHistoryRepository,
)
from src.app.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
    TaskHistoryRepositoryProtocol,
)
from src.app.application.interactors import (
    GetAllTasksInteractor,
    CreateCurrentUserTaskInteractor,
    GetCurentUserTasksInteractor,
    GetCurrentUserTaskInteractor,
    DeleteCurrentUserTaskInteractor,
    CompleteTaskInteractor,
    UpdateCurrentUserTaskInteractor,
    UncompleteTaskInteractor,
    GetDeletedTasksBySessionTokenInteractor,
    GetDailyTasksBySessionTokenInteractor,
    GetOverdueTasksInteractor,
    GetTodaysDeadlineInteractor,
    ClearExpiredTasksInteractor,
)


class TaskProvider(Provider):
    scope = Scope.REQUEST
    task_repository = provide(TaskRepository, provides=TaskRepositoryProtocol)
    task_history_repository = provide(
        TaskHistoryRepository, provides=TaskHistoryRepositoryProtocol
    )
    get_all_tasks = provide(GetAllTasksInteractor)
    get_current_user_tasks = provide(GetCurentUserTasksInteractor)
    get_task = provide(GetCurrentUserTaskInteractor)
    create_task = provide(CreateCurrentUserTaskInteractor)
    update_task = provide(UpdateCurrentUserTaskInteractor)
    delete_task = provide(DeleteCurrentUserTaskInteractor)
    complete_task = provide(CompleteTaskInteractor)
    uncomplete_task = provide(UncompleteTaskInteractor)
    get_deleted_tasks = provide(GetDeletedTasksBySessionTokenInteractor)
    get_daily_tasks = provide(GetDailyTasksBySessionTokenInteractor)
    get_overdue_tasks = provide(GetOverdueTasksInteractor)
    get_todays_deadline_tasks = provide(GetTodaysDeadlineInteractor)
    clear_expired_tasks = provide(ClearExpiredTasksInteractor)
