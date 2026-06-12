from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, HTTPException
from pydantic import UUID7

from todo_rpg.application.interactors import (
    GetCurrentUserRanksInteractor,
    GetCurrentUserRankInteractor,
    CreateCurrentUserRankInteractor,
    UpdateCurrentUserRankInteractor,
    DeleteCurrentUserRankInteractor,
)
from todo_rpg.presentation.mappers import UserRankSchemaMapper
from todo_rpg.presentation.schemas import (
    UserRankSchemaCreate,
    UserRankSchemaRead,
    UserRankSchemaUpdate,
)

router = APIRouter(prefix="/rank", route_class=DishkaRoute)


@router.get("/me", response_model=list[UserRankSchemaRead])
async def get_current_user_ranks(
    interactor: FromDishka[GetCurrentUserRanksInteractor],
    session_token=Cookie(None),
    limit: int = 20,
    offset: int = 0,
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)


@router.get("/me/{user_rank_id}", response_model=UserRankSchemaRead)
async def get_current_user_rank(
    interactor: FromDishka[GetCurrentUserRankInteractor],
    user_rank_id: UUID7,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(user_rank_id, session_token)


@router.post("/me", response_model=UserRankSchemaRead)
async def create_current_user_skill(
    interactor: FromDishka[CreateCurrentUserRankInteractor],
    schema: UserRankSchemaCreate,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserRankSchemaMapper.to_create_dto(schema)
    return await interactor(session_token, dto)


@router.patch("/me/{user_rank_id}", response_model=UserRankSchemaRead)
async def update_current_user_skill(
    interactor: FromDishka[UpdateCurrentUserRankInteractor],
    schema: UserRankSchemaUpdate,
    user_rank_id: UUID7,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserRankSchemaMapper.to_update_dto(schema)
    return await interactor(user_rank_id, session_token, dto)


@router.delete("me/{user_rank_id}", status_code=204)
async def delete_current_user_task(
    task_id: UUID7,
    interactor: FromDishka[DeleteCurrentUserRankInteractor],
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    await interactor(session_token, task_id)
