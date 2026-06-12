from todo_rpg.presentation.schemas.common import SkillRequirementsSchema, ItemSchemaRead
from pydantic import BaseModel


class ItemWithRequirementsSchema(BaseModel):
    item: ItemSchemaRead
    requirements: list[SkillRequirementsSchema]
