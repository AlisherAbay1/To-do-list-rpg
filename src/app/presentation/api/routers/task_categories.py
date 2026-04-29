from fastapi import APIRouter, Cookie
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors.task_categories import GetAllTaskCategories, GetCurrentUserTaskCategories, CreateCurrentUserTaskCategory
from src.app.presentation.schemas.task_categories import TaskCategoriesSchema, CreateTaskCategoriesSchema
from src.app.presentation.mappers import TaskCategoriesSchemaMapper

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

@router.post("/me", response_model=TaskCategoriesSchema)
async def create_current_user_task_categories(
                                              schema: CreateTaskCategoriesSchema,
                                              interactor: FromDishka[CreateCurrentUserTaskCategory], 
                                              session_token: str = Cookie(None)
                                              ):
    dto = TaskCategoriesSchemaMapper.to_create_dto(schema)
    return await interactor(session_token, dto)