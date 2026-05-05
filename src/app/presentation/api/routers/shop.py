from fastapi import APIRouter, HTTPException, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors import (
    GetCurrentUserShopListingsInteractor, 
    CreateCurrentUserShopListingInteractor, 
    UpdateCurrentUserShopListingInteractor)
from src.app.presentation.schemas import ShopListingShortSchemaRead, ShopListingSchemaCreate, ShopListingSchemaUpdate
from src.app.presentation.mappers import ShopSchemaMapper
from uuid import UUID

router = APIRouter(prefix="/shop", route_class=DishkaRoute)

@router.get("/me", response_model=list[ShopListingShortSchemaRead])
async def get_current_user_shop_listings(interactor: FromDishka[GetCurrentUserShopListingsInteractor], 
                                         session_token = Cookie(None), 
                                         limit: int = 20, 
                                         offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.post("/me", response_model=ShopListingShortSchemaRead)
async def create_current_user_shop_listing(interactor: FromDishka[CreateCurrentUserShopListingInteractor], 
                                           schema: ShopListingSchemaCreate,
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = ShopSchemaMapper.to_create_dto(schema)
    return await interactor(session_token, dto)

@router.patch("/me/{shop_listing_id}", response_model=ShopListingShortSchemaRead)
async def update_current_user_shop_listing(shop_listing_id: UUID, 
                                           interactor: FromDishka[UpdateCurrentUserShopListingInteractor], 
                                           schema: ShopListingSchemaUpdate,
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = ShopSchemaMapper.to_update_dto(schema)
    return await interactor(shop_listing_id, session_token, dto)