from src.app.application.dto.common import SkillRequirementsWithFitRequiremenetDTO
from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class ShopListingShortWithFtRequiremenetsDTO:
    id: UUID
    item_id: UUID
    price: int
    quantity: int
    fit_requirements: bool
    skill_requirements: list[SkillRequirementsWithFitRequiremenetDTO]