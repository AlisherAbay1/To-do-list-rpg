from fastapi import APIRouter, HTTPException, Cookie, Depends
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from todo_rpg.application.interactors import (
    GetShopTransactionsInteractor,
    CancelTransactionInteractor,
)
from todo_rpg.presentation.schemas import (
    ShopTransactionSchemaRead,
    ShopTransactionFilters,
)
from todo_rpg.presentation.mappers import ShopTransactionSchemaMapper
from uuid import UUID

router = APIRouter(prefix="/shop_transaction", route_class=DishkaRoute)


@router.get("/me", response_model=list[ShopTransactionSchemaRead])
async def get_shop_transactions(
    interactor: FromDishka[GetShopTransactionsInteractor],
    session_token=Cookie(None),
    limit: int = 20,
    offset: int = 0,
    filters: ShopTransactionFilters = Depends(),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    filters_dto = ShopTransactionSchemaMapper.to_filters_dto(filters)
    return await interactor(session_token, limit, offset, filters_dto)


@router.delete("/me/{shop_transaction_id}", status_code=204)
async def cancel_transacton(
    interactor: FromDishka[CancelTransactionInteractor],
    shop_transaction_id: UUID,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, shop_transaction_id)
