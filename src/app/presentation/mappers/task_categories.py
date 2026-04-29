from src.app.application.dto.task_categories import CreateTaskCategoryDTO
from src.app.presentation.schemas.task_categories import CreateTaskCategoriesSchema

class TaskCategoriesSchemaMapper: 
    @staticmethod
    def to_create_dto(schema: CreateTaskCategoriesSchema) -> CreateTaskCategoryDTO:
        dto = CreateTaskCategoryDTO(
            title=schema.title, 
            color=schema.color
        )
        return dto