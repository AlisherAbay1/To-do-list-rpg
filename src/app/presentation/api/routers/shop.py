from fastapi import APIRouter, HTTPException, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors import GetCurrentUserShopListingsInteractor

router = APIRouter(prefix="/shop", route_class=DishkaRoute)

@router.get("/me")
async def get_current_user_shop_listings(interactor: FromDishka[GetCurrentUserShopListingsInteractor], 
                                         session_token = Cookie(None), 
                                         limit: int = 20, 
                                         offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

