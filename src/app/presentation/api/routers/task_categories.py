from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors.task_categories import GetAllTaskCategories


router = APIRouter(prefix="/task_categories", route_class=DishkaRoute)

@router.get("")
async def get_all_task_categories(
    intercator: FromDishka[GetAllTaskCategories]):
    return await intercator()