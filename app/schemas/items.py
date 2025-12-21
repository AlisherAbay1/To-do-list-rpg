from pydantic import UUID7, BaseModel, ConfigDict


class ItemSchemaRead(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str
    description: str | None
    amount: int

    model_config = ConfigDict(from_attributes=True)

class ItemSchemaCreate(BaseModel):
    user_id: UUID7
    title: str
    description: str | None
    amount: int

    model_config = ConfigDict(from_attributes=True)