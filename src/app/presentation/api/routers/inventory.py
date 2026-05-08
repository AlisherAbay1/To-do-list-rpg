from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors import (
        GetCurrentUserInventoryItemByIdInteractor, 
        GetCurrentUserInventoryItemsInteractor, 
        DeleteCurrentUserInventoryItemInteractor,
        UseCurrentUserInventoryItemInteractor 
    )
from src.app.presentation.schemas import (InventorySchemaRead, InventoryShortSchemaRead, InventoryShortWithItemSchemaRead)
from uuid import UUID

router = APIRouter(prefix="/inventory", route_class=DishkaRoute)

@router.get("/me", response_model=list[InventoryShortSchemaRead])
async def get_current_user_inventory_items(interactor: FromDishka[GetCurrentUserInventoryItemsInteractor], 
                                         session_token = Cookie(None), 
                                         limit: int = 20, 
                                         offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.get("/me/{inventory_item_id}", response_model=InventoryShortWithItemSchemaRead)
async def get_current_user_inventory_item_by_id(interactor: FromDishka[GetCurrentUserInventoryItemByIdInteractor], 
                                              inventory_item_id: UUID,
                                              session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, inventory_item_id)

@router.post("/me/{inventory_item_id}/use", response_model=InventoryShortWithItemSchemaRead)
async def use_current_user_inventory_item_by_id(interactor: FromDishka[UseCurrentUserInventoryItemInteractor], 
                                              inventory_item_id: UUID,
                                              session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, inventory_item_id)

@router.delete("/me/{inventory_item_id}", status_code=204)
async def delete_current_user_inventory_item(inventory_item_id: UUID, 
                                           interactor: FromDishka[DeleteCurrentUserInventoryItemInteractor], 
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(inventory_item_id, session_token)
