from fastapi import APIRouter, Cookie, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.app.application.interactors.task_categories import GetAllTaskCategories, GetCurrentUserTaskCategories, CreateCurrentUserTaskCategory, \
                                                            UpdateCurrentUserTaskCategory
from src.app.presentation.schemas.task_categories import TaskCategoriesSchema, CreateTaskCategorySchema, UpdateTaskCategorySchema
from src.app.presentation.mappers import TaskCategoriesSchemaMapper
from uuid import UUID

router = APIRouter(prefix="/task_categories", route_class=DishkaRoute)

@router.get("", response_model=list[TaskCategoriesSchema])
async def get_all_task_categories(intercator: FromDishka[GetAllTaskCategories]):
    return await intercator()

@router.get("/me", response_model=list[TaskCategoriesSchema])
async def get_current_user_task_catigories(interactor: FromDishka[GetCurrentUserTaskCategories], 
                                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token)

@router.post("/me", response_model=TaskCategoriesSchema)
async def create_current_user_task_category(schema: CreateTaskCategorySchema,
                                            interactor: FromDishka[CreateCurrentUserTaskCategory], 
                                            session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskCategoriesSchemaMapper.to_create_dto(schema)
    return await interactor(session_token, dto)

@router.patch("/me", response_model=TaskCategoriesSchema)
async def update_current_user_task_category(task_category_id: UUID, 
                                            schema: UpdateTaskCategorySchema, 
                                            interactor: FromDishka[UpdateCurrentUserTaskCategory], 
                                            session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskCategoriesSchemaMapper.to_update_dto(schema)
    return await interactor(task_category_id, dto, session_token)