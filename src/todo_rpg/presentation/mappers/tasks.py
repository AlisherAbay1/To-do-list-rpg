from todo_rpg.presentation.schemas import (
    TaskFilterParams,
    TaskSortParams,
    TaskSchemaCreate,
    TaskSchemaUpdate,
)
from todo_rpg.application.dto import (
    TaskFilterParamsDTO,
    TaskSortParamsDTO,
    TaskCreateDTO,
    TaskUpdateDTO,
)
from todo_rpg.application.dto.sentinel_types import UNSET


class TaskSchemaMapper:
    @staticmethod
    def to_filter_params_dto(schema: TaskFilterParams) -> TaskFilterParamsDTO:
        dto = TaskFilterParamsDTO(
            difficulty=schema.difficulty,
            priority=schema.priority,
            type=schema.type,
            repeat_frequency=schema.repeat_frequency,
            deleted=schema.deleted,
        )
        return dto

    @staticmethod
    def to_sorting_params_dto(schema: TaskSortParams) -> TaskSortParamsDTO:
        dto = TaskSortParamsDTO(sort_by=schema.sort_by, sort_order=schema.sort_order)
        return dto

    @staticmethod
    def to_create_dto(schema: TaskSchemaCreate) -> TaskCreateDTO:
        dto = TaskCreateDTO(
            title=schema.title,
            description=schema.description,
            category_id=schema.category_id,
            repeat_limit=schema.repeat_limit,
            repeat_frequency=schema.repeat_frequency,
            deadline=schema.deadline,
            type=schema.type,
            difficulty=schema.difficulty,
            priority=schema.priority,
            custom_xp_reward=schema.custom_xp_reward,
            custom_gold_reward=schema.custom_gold_reward,
            related_skills=schema.related_skills,
            related_items=schema.related_items,
        )
        return dto

    @staticmethod
    def to_update_dto(schema: TaskSchemaUpdate) -> TaskUpdateDTO:
        clean_data = schema.model_dump(exclude_unset=True)
        dto = TaskUpdateDTO(
            title=clean_data.get("title", UNSET),
            description=clean_data.get("description", UNSET),
            category_id=clean_data.get("category_id", UNSET),
            repeat_limit=clean_data.get("repeat_limit", UNSET),
            repeat_frequency=clean_data.get("repeat_frequency", UNSET),
            deadline=clean_data.get("deadline", UNSET),
            type=clean_data.get("type", UNSET),
            difficulty=clean_data.get("difficulty", UNSET),
            priority=clean_data.get("priority", UNSET),
            custom_xp_reward=clean_data.get("custom_xp_reward", UNSET),
            custom_gold_reward=clean_data.get("custom_gold_reward", UNSET),
            deleted=clean_data.get("deleted", UNSET),
        )
        return dto
