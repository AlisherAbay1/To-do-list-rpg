from src.app.domain import Item
from src.app.application.dto import ItemDTO, ItemWithRequirementsDTO, SkillRequirementsDTO, SkillShortDTO
from typing import Sequence

class ItemMapper:
    @staticmethod
    def to_dto(domain: Item) -> ItemDTO:
        dto = ItemDTO(
            id=domain.id,
            user_id=domain.user_id, 
            title=domain.title, 
            description=domain.description, 
            deleted=domain.deleted, 
            deleted_at=domain.deleted_at
        )
        return dto
    
    @staticmethod
    def to_list_dto(domains: Sequence) -> list[ItemDTO]:
        return [ItemMapper.to_dto(domain) for domain in domains]
    
