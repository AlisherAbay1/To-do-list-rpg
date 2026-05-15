from src.app.presentation.schemas import (
    ShopListingSchemaCreate,
    ShopListingSchemaUpdate,
)
from src.app.application.dto import ShopListingCreateDTO, ShopListingUpdateDTO
from src.app.application.dto.sentinel_types import UNSET


class ShopSchemaMapper:
    @staticmethod
    def to_create_dto(schema: ShopListingSchemaCreate) -> ShopListingCreateDTO:
        dto = ShopListingCreateDTO(
            item_id=schema.item_id, price=schema.price, quantity=schema.quantity
        )
        return dto

    @staticmethod
    def to_update_dto(schema: ShopListingSchemaUpdate) -> ShopListingUpdateDTO:
        clean_data = schema.model_dump(exclude_unset=True)
        dto = ShopListingUpdateDTO(
            price=clean_data.get("price", UNSET),
            quantity=clean_data.get("quantity", UNSET),
        )
        return dto
