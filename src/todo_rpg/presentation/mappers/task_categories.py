from todo_rpg.application.dto import CreateTaskCategoryDTO, UpdateTaskCategoryDTO
from todo_rpg.presentation.schemas import (
    CreateTaskCategorySchema,
    UpdateTaskCategorySchema,
)
from todo_rpg.application.dto.sentinel_types import UNSET


class TaskCategoriesSchemaMapper:
    @staticmethod
    def to_create_dto(schema: CreateTaskCategorySchema) -> CreateTaskCategoryDTO:
        dto = CreateTaskCategoryDTO(title=schema.title, color=schema.color)
        return dto

    @staticmethod
    def to_update_dto(schema: UpdateTaskCategorySchema) -> UpdateTaskCategoryDTO:
        data = schema.model_dump(exclude_unset=True)
        dto = UpdateTaskCategoryDTO(
            title=data.get("title") or UNSET, color=data.get("color") or UNSET
        )
        return dto
