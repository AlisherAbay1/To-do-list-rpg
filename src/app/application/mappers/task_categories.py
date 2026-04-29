from src.app.domain import TaskCategory
from src.app.application.dto.task_categories import TaskCategoriesDTO
from typing import Sequence

class TaskCategoriesMapper:
    @staticmethod
    def to_dto(domain: TaskCategory) -> TaskCategoriesDTO:
        task_categories = TaskCategoriesDTO(
            id=domain.id, 
            user_id=domain.user_id, 
            title=domain.title, 
            color=domain.color
        )
        return task_categories
    
    @staticmethod
    def to_list_dto(domains: Sequence[TaskCategory]) -> list[TaskCategoriesDTO]:
        return [TaskCategoriesMapper.to_dto(domain) for domain in domains]