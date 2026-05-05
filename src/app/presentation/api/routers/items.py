from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Cookie
from pydantic import UUID7

from src.app.application.interactors import (CreateCurrentUserItemInteractor,
                                             DeleteItemInteractor,
                                             GetAllItemsInteractor,
                                             GetCurrentUserItemsInteractor,
                                             GetItemInteractor, 
                                             GetCurrentUserItemInteractor)
from src.app.presentation.mappers import ItemSchemaMapper
from src.app.presentation.schemas import ItemSchemaCreate, ItemSchemaRead, ItemWithRequirementsSchema

router = APIRouter(prefix="/item", route_class=DishkaRoute)

@router.get("", response_model=list[ItemSchemaRead])
async def get_all_items(interactor: FromDishka[GetAllItemsInteractor], 
                        limit: int = 20, 
                        offset: int = 0):
    return await interactor(limit, offset)

@router.get("/me", response_model=list[ItemSchemaRead])
async def get_current_user_items(interactor: FromDishka[GetCurrentUserItemsInteractor], 
                                 get_deleted: bool,
                                 session_token = Cookie(None),
                                 limit: int = 20, 
                                 offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset, get_deleted)

@router.post("/me", response_model=ItemSchemaRead)
async def create_current_user_item(data: ItemSchemaCreate, 
                                   interactor: FromDishka[CreateCurrentUserItemInteractor], 
                                   session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = ItemSchemaMapper.to_create_dto(data)
    return await interactor(session_token, dto)

@router.get("/me/{item_id}", response_model=ItemWithRequirementsSchema)
async def get_current_user_item(item_id: UUID7, 
                                interactor: FromDishka[GetCurrentUserItemInteractor], 
                                session_token = Cookie(None)):
    return await interactor(item_id, session_token)

@router.get("/{item_id}", response_model=ItemSchemaRead)
async def get_item(item_id: UUID7, 
                   interactor: FromDishka[GetItemInteractor]):
    return await interactor(item_id)

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: UUID7,
                      interactor: FromDishka[DeleteItemInteractor]):
    return await interactor(item_id)
