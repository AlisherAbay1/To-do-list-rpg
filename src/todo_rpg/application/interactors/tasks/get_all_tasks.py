from todo_rpg.application.dto import TaskFilterParamsDTO, TaskSortParamsDTO
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)
from todo_rpg.application.mappers import TaskMapper
from todo_rpg.application.dto import TaskDetailDTO


class GetAllTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(
        self,
        filters: TaskFilterParamsDTO,
        sorting: TaskSortParamsDTO,
        limit: int,
        offset: int,
    ) -> list[TaskDetailDTO]:
        tasks = await self.repo.get_all_tasks(filters, sorting, limit, offset)
        dtos = TaskMapper.to_list_detail_dto(tasks)
        return dtos
