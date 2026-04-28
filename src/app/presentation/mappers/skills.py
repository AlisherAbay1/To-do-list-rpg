from src.app.presentation.schemas import SkillSchemaCreate, SkillSchemaRead
from src.app.application.dto.skills import SkillCreateDTO

class SkillSchemaMapper:
    @staticmethod
    def to_create_dto(schema: SkillSchemaCreate) -> SkillCreateDTO:
        dto = SkillCreateDTO(
            title=schema.title,
            description=schema.description, 
            ico=schema.ico, 
            lvl=schema.lvl, 
            xp=schema.xp
        )
        return dto