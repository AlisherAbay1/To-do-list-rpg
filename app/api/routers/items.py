from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import UUID7
from app.schemas import ItemSchemaCreate, ItemSchemaRead, ItemCreateDTO
from app.services.interactors import GetAllItemsInteractor, GetCurrentUserItemsInteractor, CreateCurrentUserItemInteractor, \
                                    GetItemInteractor, DeleteItemInteractor
from dishka.integrations.fastapi import FromDishka, DishkaRoute

router = APIRouter(prefix="/item", route_class=DishkaRoute)

@router.get("", response_model=list[ItemSchemaRead])
async def get_all_items(interactor: FromDishka[GetAllItemsInteractor], 
                        limit: int = 20, 
                        offset: int = 0):
    return await interactor(limit, offset)

@router.get("/me", response_model=list[ItemSchemaRead])
async def get_current_user_items(interactor: FromDishka[GetCurrentUserItemsInteractor], 
                                 request: Request, 
                                 limit: int = 20, 
                                 offset: int = 0):
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_id, limit, offset)

@router.post("/me", response_model=ItemSchemaRead)
async def create_current_user_item(data: ItemSchemaCreate, 
                                   request: Request, 
                                   interactor: FromDishka[CreateCurrentUserItemInteractor]):
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    dto = ItemCreateDTO(
        title=data.title, 
        description=data.description
    )
    return await interactor(session_id, dto)

@router.get("/{item_id}", response_model=ItemSchemaRead)
async def get_item(item_id: UUID7, 
                   interactor: FromDishka[GetItemInteractor]):
    return await interactor(item_id)

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: UUID7,
                      interactor: FromDishka[DeleteItemInteractor]):
    return await interactor(item_id)
