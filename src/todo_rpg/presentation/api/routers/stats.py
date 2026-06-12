from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, HTTPException
from todo_rpg.application.interactors import GetStatsOverviewInteractor

router = APIRouter(prefix="/stats", route_class=DishkaRoute)


@router.get("/overview")
async def get_stats_overview(
    interactor: FromDishka[GetStatsOverviewInteractor], session_token=Cookie(None)
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token)
