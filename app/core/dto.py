from app.models import Base
from pydantic import BaseModel
from sqlalchemy import ScalarResult
from fastapi import HTTPException
from typing import TypeVar, Optional

model_base = TypeVar("model_base", bound=Base)
schema_base = TypeVar("schema_base", bound=BaseModel)

def model_to_dto(model: Optional[Base], schema: type[schema_base]) -> schema_base:
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return schema.model_validate(model, from_attributes=True)

def models_to_dtos(models: ScalarResult[model_base], schema: type[schema_base]) -> list[schema_base]:
    return [schema.model_validate(model, from_attributes=True) for model in models if model is not None ]