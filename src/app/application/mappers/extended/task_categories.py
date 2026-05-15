from src.app.domain import TaskCategory, Task
from src.app.application.dto import TaskCategoryWithTasksDTO
from typing import Sequence
from src.app.application.mappers.common import TaskMapper


class ExtendedTaskCategoriesMapper:
    @staticmethod
    def to_dto_with_tasks(
        domain: TaskCategory, task_domains: Sequence[Task]
    ) -> TaskCategoryWithTasksDTO:
        dto = TaskCategoryWithTasksDTO(
            id=domain.id,
            user_id=domain.user_id,
            title=domain.title,
            color=domain.color,
            tasks=TaskMapper.to_list_detail_dto(task_domains),
        )
        return dto
