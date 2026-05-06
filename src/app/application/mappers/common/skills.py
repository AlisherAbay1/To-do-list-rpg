from src.app.domain import Skill
from src.app.application.dto.common.skills import SkillDTO, SkillShortDTO, SkillRequirementsWithFitRequiremenetDTO
from typing import Sequence

class SkillMapper:
    @staticmethod
    def to_dto(domain: Skill) -> SkillDTO:
        dto = SkillDTO(
            id=domain.id,
            user_id=domain.user_id, 
            title=domain.title, 
            description=domain.description, 
            ico=domain.ico, 
            lvl=domain.lvl, 
            xp=domain.xp, 
            deleted=domain.deleted, 
            deleted_at=domain.deleted_at
        )
        return dto
    
    @staticmethod
    def to_list_dto(domains: Sequence) -> list[SkillDTO]:
        return [SkillMapper.to_dto(domain) for domain in domains]
    
    @staticmethod
    def to_short_dto(domain: Skill) -> SkillShortDTO:
        dto = SkillShortDTO(
            id=domain.id,
            title=domain.title, 
            description=domain.description, 
            ico=domain.ico, 
            lvl=domain.lvl, 
            xp=domain.xp
        )
        return dto