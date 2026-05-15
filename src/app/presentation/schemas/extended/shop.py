from src.app.presentation.schemas.common import (
    SkillRequirementsWithFitRequiremenetSchema,
    ShopListingShortSchemaRead,
    InventoryShortSchemaRead,
)
from pydantic import BaseModel
from uuid import UUID


class ShopListingShortWithFitRequiremenetsSchema(BaseModel):
    id: UUID
    item_id: UUID
    price: int
    quantity: int
    fit_requirements: bool
    skill_requirements: list[SkillRequirementsWithFitRequiremenetSchema]


class ShopListingShortWithShortInventoryItemSchema(BaseModel):
    shop_listing: ShopListingShortSchemaRead
    inventory_item: InventoryShortSchemaRead
    balance: int
