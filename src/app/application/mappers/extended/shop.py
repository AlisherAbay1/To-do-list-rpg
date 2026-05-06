from src.app.domain import Shop, Item
from src.app.application.dto import ShopListingShortWithFtRequiremenetsDTO, SkillRequirementsWithFitRequiremenetDTO
from typing import Sequence
from src.app.application.mappers import SkillMapper

class ExtendedShopMapper:
    @staticmethod
    def to_shop_listing_with_fit_requirement(shop_domain: Shop, item_domain: Item):
        dto = ShopListingShortWithFtRequiremenetsDTO(
                id=shop_domain.id, 
                item_id=shop_domain.item_id, 
                price=shop_domain.price, 
                quantity=shop_domain.quantity, 
                fit_requirements=item_domain.does_fit_requirements(), 
                skill_requirements=[SkillRequirementsWithFitRequiremenetDTO(
                                    skill=SkillMapper.to_short_dto(requirement_domain.skill), 
                                    required_lvl=requirement_domain.required_lvl,
                                    fit_requirement=requirement_domain.does_fit_requirement()
                ) for requirement_domain in item_domain.requirements]
        )
        return dto