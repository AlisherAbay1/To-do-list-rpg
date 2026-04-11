from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.dto.tasks import TaskFilterParamsDTO, TaskSortParamsDTO

class GetAllTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, filters: TaskFilterParamsDTO, sorting: TaskSortParamsDTO, limit: int, offset: int):
        tasks = await self.repo.get_all_tasks(filters, sorting, limit, offset)
        return list(tasks)