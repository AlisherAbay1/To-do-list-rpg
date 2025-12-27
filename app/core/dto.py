from app.models import Base
from pydantic import BaseModel
from sqlalchemy import ScalarResult
from fastapi import HTTPException
from typing import TypeVar, Optional

model_base = TypeVar("model_base", bound=Base)

def model_to_dto(model: Optional[Base], schema: type[BaseModel]):
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return schema.model_validate(model)

def models_to_dtos(models: ScalarResult[model_base], schema: type[BaseModel]):
    return [schema.model_validate(model) for model in models if model is not None ]