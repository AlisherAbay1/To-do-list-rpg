from src.app.presentation.schemas import SkillRequirementsWithFitRequiremenetSchema
from pydantic import BaseModel
from uuid import UUID

class ShopListingShortWithFitRequiremenetsSchema(BaseModel):
    id: UUID
    item_id: UUID
    price: int
    quantity: int
    fit_requirements: bool
    skill_requirements: list[SkillRequirementsWithFitRequiremenetSchema]