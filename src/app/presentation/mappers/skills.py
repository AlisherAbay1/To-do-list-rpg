from src.app.presentation.schemas import SkillSchemaCreate, SkillSchemaUpdate
from src.app.application.dto import SkillCreateDTO, SkillUpdateDTO
from src.app.application.dto.sentinel_types import UNSET


class SkillSchemaMapper:
    @staticmethod
    def to_create_dto(schema: SkillSchemaCreate) -> SkillCreateDTO:
        dto = SkillCreateDTO(
            title=schema.title,
            description=schema.description,
            ico=schema.ico,
            lvl=schema.lvl,
            xp=schema.xp,
        )
        return dto

    @staticmethod
    def to_update_dto(schema: SkillSchemaUpdate) -> SkillUpdateDTO:
        clean_data = schema.model_dump(exclude_unset=True)
        dto = SkillUpdateDTO(
            title=clean_data.get("title", UNSET),
            description=clean_data.get("description", UNSET),
            ico=clean_data.get("ico", UNSET),
            lvl=clean_data.get("lvl", UNSET),
            xp=clean_data.get("xp", UNSET),
        )
        return dto
