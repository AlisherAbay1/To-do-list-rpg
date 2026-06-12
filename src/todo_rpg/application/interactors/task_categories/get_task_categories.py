from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.mappers.common import TaskCategoriesMapper
from todo_rpg.application.dto import TaskCategoryDTO


class GetAllTaskCategories:
    def __init__(self, repo: TaskCategoriesRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self) -> list[TaskCategoryDTO]:
        task_categories = await self.repo.get_all_task_categories()
        return TaskCategoriesMapper.to_list_dto(task_categories)
