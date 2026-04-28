from src.app.presentation.schemas import ItemSchemaCreate
from src.app.application.dto.items import ItemCreateDTO

class ItemSchemaMapper:
    @staticmethod
    def to_create_dto(schema: ItemSchemaCreate) -> ItemCreateDTO:
        dto = ItemCreateDTO(
            title=schema.title, 
            description=schema.description
        )
        return dto