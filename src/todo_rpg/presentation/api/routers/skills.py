from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, HTTPException
from pydantic import UUID7

from todo_rpg.application.interactors import (
    CreateCurrentUserSkillInteractor,
    DeleteSkillInteractor,
    GetAllSkillsInteractor,
    GetCurrentUserSkillsInteractor,
    GetSkillInteractor,
    DeleteCurrentUserSkillByIdInteractor,
    GetCurrentUserSkillByIdInteractor,
    UpdateCurrentUserSkillById,
)
from todo_rpg.presentation.mappers import SkillSchemaMapper
from todo_rpg.presentation.schemas import (
    SkillSchemaCreate,
    SkillSchemaRead,
    SkillWithTasksAndNextLvlXpSchemaRead,
    SkillSchemaUpdate,
)

router = APIRouter(prefix="/skill", route_class=DishkaRoute)


@router.get("", response_model=list[SkillSchemaRead])
async def get_all_skills(
    interactor: FromDishka[GetAllSkillsInteractor], limit: int = 20, offset: int = 0
):
    return await interactor(limit, offset)


@router.get("/me", response_model=list[SkillSchemaRead])
async def get_current_user_skills(
    interactor: FromDishka[GetCurrentUserSkillsInteractor],
    session_token=Cookie(None),
    limit: int = 20,
    offset: int = 0,
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)


@router.post("/me", response_model=SkillSchemaRead)
async def create_current_user_skill(
    interactor: FromDishka[CreateCurrentUserSkillInteractor],
    data: SkillSchemaCreate,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = SkillSchemaMapper.to_create_dto(data)
    return await interactor(session_token, dto)


@router.delete("/me/{skill_id}", status_code=204)
async def delete_current_user_skill(
    skill_id: UUID7,
    interactor: FromDishka[DeleteCurrentUserSkillByIdInteractor],
    session_token=Cookie(None),
):
    await interactor(skill_id, session_token)


@router.get("/me/{skill_id}", response_model=SkillWithTasksAndNextLvlXpSchemaRead)
async def get_current_user_skill_by_id(
    skill_id: UUID7,
    interactor: FromDishka[GetCurrentUserSkillByIdInteractor],
    get_related_tasks: bool,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(skill_id, session_token, get_related_tasks)


@router.patch("/me/{skill_id}", response_model=SkillSchemaRead)
async def update_current_user_skill_by_id(
    skill_id: UUID7,
    data: SkillSchemaUpdate,
    interactor: FromDishka[UpdateCurrentUserSkillById],
    session_token=Cookie(None),
):
    dto = SkillSchemaMapper.to_update_dto(data)
    return await interactor(skill_id, dto, session_token)


@router.get("/{skill_id}", response_model=SkillSchemaRead)
async def get_skill(
    skill_id: UUID7,
    interactor: FromDishka[GetSkillInteractor],
):
    return await interactor(skill_id)


@router.delete("/{skill_id}", status_code=204)
async def delete_skill(skill_id: UUID7, interactor: FromDishka[DeleteSkillInteractor]):
    await interactor(skill_id)
