from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors import (
    
    )
from src.app.presentation.schemas import 
from src.app.presentation.mappers import InventorySchemaMapper
from uuid import UUID

router = APIRouter(prefix="/inventory", route_class=DishkaRoute)

@router.get("/me", response_model=...)
async def get_current_user_inventory_item(interactor: FromDishka[...], 
                                         session_token = Cookie(None), 
                                         limit: int = 20, 
                                         offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.get("/me/{inventory_item_id}", response_model=...)
async def get_current_user_inventory_item_by_id(interactor: FromDishka[...], 
                                              inventory_item_id: UUID,
                                              session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, inventory_item_id)

@router.post("/me", response_model=...)
async def create_current_user_inventory_itemg(interactor: FromDishka[...], 
                                           schema: ...,
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = InventorySchemaMapper.to_create_dto(schema)
    return await interactor(session_token, dto)

@router.patch("/me/{inventory_item_id}", response_model=...)
async def update_current_user_inventory_item(inventory_item_id: UUID, 
                                           interactor: FromDishka[...], 
                                           schema: ...,
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = InventorySchemaMapper.to_update_dto(schema)
    return await interactor(inventory_item_id, session_token, dto)

@router.delete("/me/{inventory_item_id}", status_code=204)
async def delete_current_user_inventory_item(inventory_item_id: UUID, 
                                           interactor: FromDishka[...], 
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(inventory_item_id, session_token)
