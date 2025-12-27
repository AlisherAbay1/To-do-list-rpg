from fastapi import APIRouter, Depends, Request
from pydantic import UUID7
from app.schemas import ItemSchemaCreate, ItemSchemaRead, ItemSchemaPatch
from app.repositories.items import ItemCRUD
from app.core.dto import model_to_dto, models_to_dtos
from app.core.session import get_user_id_by_session
from app.models.items import Item

router = APIRouter(prefix="/item")

@router.get("")
def get_all_items(limit: int = 20, offset: int = 0, crud: ItemCRUD = Depends()):
    selected = crud.select_many(limit, offset)
    return models_to_dtos(selected, ItemSchemaRead)

@router.post("")
def create_item(data: ItemSchemaCreate, request: Request, crud: ItemCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = get_user_id_by_session(request)
    return model_to_dto(crud.insert(**info), ItemSchemaRead)

@router.get("/{item_id}")
def get_item(item_id: UUID7, crud: ItemCRUD = Depends()):
    selected = crud.select(Item.id == item_id)
    return model_to_dto(selected, ItemSchemaRead)

@router.patch("/{item_id}")
def update_item(item_id: UUID7, data: ItemSchemaPatch, crud: ItemCRUD = Depends()):
    info = data.model_dump(exclude_unset=True)
    updated = crud.update(Item.id == item_id, **info)
    return model_to_dto(updated, ItemSchemaRead)

@router.delete("/{item_id}")
def delete_item(item_id: UUID7, crud: ItemCRUD = Depends()):
    deleted = crud.delete(Item.id == item_id)
    return model_to_dto(deleted, ItemSchemaRead)
