from fastapi import APIRouter, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors.task_categories import GetAllTaskCategories, GetCurrentUserTaskCategories
from src.app.presentation.schemas.task_categories import TaskCategoriesSchema

router = APIRouter(prefix="/task_categories", route_class=DishkaRoute)

@router.get("", response_model=list[TaskCategoriesSchema])
async def get_all_task_categories(
                                  intercator: FromDishka[GetAllTaskCategories]):
    return await intercator()

@router.get("/me", response_model=list[TaskCategoriesSchema])
async def get_current_user_task_catigories(
                                          interactor: FromDishka[GetCurrentUserTaskCategories], 
                                          session_token: str = Cookie(None)):
    return await interactor(session_token)

