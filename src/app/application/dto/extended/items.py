from src.app.application.dto.common import ItemDTO, SkillRequirementsDTO
from dataclasses import dataclass

@dataclass
class ItemWithRequirementsDTO:
    item: ItemDTO
    requirements: list[SkillRequirementsDTO]