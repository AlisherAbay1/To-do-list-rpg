from src.app.domain import TaskCategory, Task
from src.app.application.dto.task_categories import TaskCategoryDTO, TaskCategoryWithTasksDTO
from typing import Sequence
from src.app.application.mappers import TaskMapper

class TaskCategoriesMapper:
    @staticmethod
    def to_dto(domain: TaskCategory) -> TaskCategoryDTO:
        task_categories = TaskCategoryDTO(
            id=domain.id, 
            user_id=domain.user_id, 
            title=domain.title, 
            color=domain.color
        )
        return task_categories
    
    @staticmethod
    def to_list_dto(domains: Sequence[TaskCategory]) -> list[TaskCategoryDTO]:
        return [TaskCategoriesMapper.to_dto(domain) for domain in domains]
    
    @staticmethod
    def to_dto_with_tasks(domain: TaskCategory, task_domains: Sequence[Task]) -> TaskCategoryWithTasksDTO:
        dto = TaskCategoryWithTasksDTO(
            id=domain.id, 
            user_id=domain.user_id, 
            title=domain.title, 
            color=domain.color, 
            tasks=TaskMapper.to_list_detail_dto(task_domains)
        )
        return dto