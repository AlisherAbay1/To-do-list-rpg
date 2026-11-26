from todo_rpg.presentation.schemas.common import (
    SkillRequirementsWithFitRequirementSchema,
    ShopListingShortSchemaRead,
    InventoryShortSchemaRead,
)
from pydantic import BaseModel
from uuid import UUID


class ShopListingShortWithFitRequirementsSchema(BaseModel):
    id: UUID
    item_id: UUID
    price: int
    quantity: int
    fit_requirements: bool
    skill_requirements: list[SkillRequirementsWithFitRequirementSchema]


class ShopListingShortWithShortInventoryItemSchema(BaseModel):
    shop_listing: ShopListingShortSchemaRead
    inventory_item: InventoryShortSchemaRead
    balance: int
