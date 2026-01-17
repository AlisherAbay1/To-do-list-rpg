from fastapi import APIRouter, Depends, Request
from pydantic import UUID7
from app.schemas import ItemSchemaCreate, ItemSchemaRead, ItemSchemaPatch
from app.repositories.items import ItemCRUD
from app.core.dto import model_to_dto, models_to_dtos
from app.core.session import get_user_id_by_session
from app.models.items import Item

router = APIRouter(prefix="/item")

@router.get("")
async def get_all_items(limit: int = 20, offset: int = 0, crud: ItemCRUD = Depends()):
    selected = crud.select_many(limit, offset)
    return models_to_dtos(await selected, ItemSchemaRead)

@router.post("")
async def create_item(data: ItemSchemaCreate, request: Request, crud: ItemCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = await get_user_id_by_session(request)
    return model_to_dto(await crud.insert(**info), ItemSchemaRead)

@router.get("/me")
async def get_current_user_items(request: Request, limit: int = 20, offset: int = 0, crud: ItemCRUD = Depends()):
    user_id = await get_user_id_by_session(request)
    return models_to_dtos(await crud.select_many(limit, offset, Item.user_id == user_id), ItemSchemaRead)

@router.post("/me")
async def create_current_user_item(data: ItemSchemaCreate, request: Request, crud: ItemCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = await get_user_id_by_session(request)
    return model_to_dto(await crud.insert(**info), ItemSchemaRead)

@router.get("/{item_id}")
async def get_item(item_id: UUID7, request: Request, crud: ItemCRUD = Depends()):
    selected = crud.select(
        Item.user_id == await get_user_id_by_session(request), 
        Item.id == item_id)
    return model_to_dto(await selected, ItemSchemaRead)

@router.patch("/{item_id}")
async def update_item(item_id: UUID7, request: Request, data: ItemSchemaPatch, crud: ItemCRUD = Depends()):
    info = data.model_dump(exclude_unset=True)
    updated = crud.update(
        Item.user_id == await get_user_id_by_session(request), 
        Item.id == item_id, 
        **info)
    return model_to_dto(await updated, ItemSchemaRead)

@router.delete("/{item_id}")
async def delete_item(item_id: UUID7, request: Request, crud: ItemCRUD = Depends()):
    deleted = crud.delete(
        Item.user_id == await get_user_id_by_session(request), 
        Item.id == item_id)
    return model_to_dto(await deleted, ItemSchemaRead)
