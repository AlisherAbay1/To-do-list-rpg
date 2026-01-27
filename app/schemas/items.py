from pydantic import UUID7, BaseModel, ConfigDict
from typing import Optional


class ItemSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str
    description: Optional[str]
    amount: int

    model_config = ConfigDict(from_attributes=True)

class ItemSchemaCreate(BaseModel):
    title: str
    description: Optional[str]
    amount: int

    model_config = ConfigDict(from_attributes=True)

