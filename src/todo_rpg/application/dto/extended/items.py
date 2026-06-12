from todo_rpg.application.dto.common import ItemDTO, SkillRequirementsDTO
from dataclasses import dataclass


@dataclass
class ItemWithRequirementsDTO:
    item: ItemDTO
    requirements: list[SkillRequirementsDTO]
