from src.app.presentation.schemas import ItemSchemaCreate, ItemSchemaUpdate
from src.app.application.dto import ItemCreateDTO, ItemUpdateDTO
from src.app.application.dto.sentinel_types import UNSET

class ItemSchemaMapper:
    @staticmethod
    def to_create_dto(schema: ItemSchemaCreate) -> ItemCreateDTO:
        dto = ItemCreateDTO(
            title=schema.title, 
            description=schema.description
        )
        return dto
    
    @staticmethod
    def to_update_dto(schema: ItemSchemaUpdate) -> ItemUpdateDTO:
        clean_data = schema.model_dump(exclude_unset=True)
        dto = ItemUpdateDTO(
            title=clean_data.get("title", UNSET), 
            description=clean_data.get("description", UNSET)
        )
        return dto