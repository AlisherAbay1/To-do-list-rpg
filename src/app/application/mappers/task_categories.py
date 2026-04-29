from src.app.domain import TaskCategory
from src.app.application.dto.task_categories import TaskCategoryDTO
from typing import Sequence

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