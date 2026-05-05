from src.app.presentation.schemas import ShopListingSchemaCreate
from src.app.application.dto import ShopListingCreateDTO
from src.app.application.dto.sentinel_types import UNSET

class ShopSchemaMapper:
    @staticmethod
    def to_create_dto(schema: ShopListingSchemaCreate) -> ShopListingCreateDTO:
        dto = ShopListingCreateDTO(
            item_id=schema.item_id, 
            price=schema.price, 
            quantity=schema.quantity
        )
        return dto