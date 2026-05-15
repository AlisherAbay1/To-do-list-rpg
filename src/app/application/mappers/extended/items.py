from src.app.domain import Item
from src.app.application.dto import ItemWithRequirementsDTO, SkillRequirementsDTO
from src.app.application.mappers.common import SkillMapper, ItemMapper


class ItemExtendedMapper:
    @staticmethod
    def to_dto_with_requirements(domain: Item) -> ItemWithRequirementsDTO:
        dto = ItemWithRequirementsDTO(
            item=ItemMapper.to_dto(domain),
            requirements=[
                SkillRequirementsDTO(
                    skill=SkillMapper.to_short_dto(requirement.skill),
                    required_lvl=requirement.required_lvl,
                )
                for requirement in domain.requirements
            ],
        )
        return dto
