from todo_rpg.presentation.schemas import UserRankSchemaCreate, UserRankSchemaUpdate
from todo_rpg.application.dto import UserRankCreateDTO, UserRankUpdateDTO
from todo_rpg.application.dto.sentinel_types import UNSET


class UserRankSchemaMapper:
    @staticmethod
    def to_create_dto(schema: UserRankSchemaCreate):
        dto = UserRankCreateDTO(title=schema.title)
        return dto

    @staticmethod
    def to_update_dto(schema: UserRankSchemaUpdate):
        clean_data = schema.model_dump(exclude_unset=True)
        dto = UserRankUpdateDTO(title=clean_data.get("title", UNSET))
        return dto
