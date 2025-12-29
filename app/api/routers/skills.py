from fastapi import APIRouter, Depends, Request, HTTPException
from app.schemas import SkillSchemaCreate, SkillSchemaRead, SkillSchemaPatch
from pydantic import UUID7
from app.repositories.skills import SkillCRUD
from app.core.session import get_user_id_by_session
from app.core.dto import models_to_dtos, model_to_dto
from app.models.skills import Skill

router = APIRouter(prefix="/skill")

@router.get("")
async def get_all_skills(limit: int = 20, offset: int = 0, crud: SkillCRUD = Depends()):
    return models_to_dtos(await crud.select_many(limit, offset), SkillSchemaRead)

@router.post("")
async def create_skill(data: SkillSchemaCreate, request: Request, crud: SkillCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = get_user_id_by_session(request)
    return crud.insert(**info)

@router.get("/me")
async def get_current_user_skills(request: Request, limit: int = 20, offset: int = 0, crud: SkillCRUD = Depends()):
    user_id = get_user_id_by_session(request)
    return models_to_dtos(await crud.select_many(limit, offset, Skill.user_id == user_id), SkillSchemaRead)

@router.post("/me")
async def create_current_user_skill(data: SkillSchemaCreate, request: Request, crud: SkillCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = get_user_id_by_session(request)
    return model_to_dto(await crud.insert(**info), SkillSchemaRead)

@router.get("/{skill_id}")
async def get_skill(skill_id: UUID7, request: Request, crud: SkillCRUD = Depends()):
    selected = crud.select(
        Skill.user_id == get_user_id_by_session(request), 
        Skill.id == skill_id)
    return model_to_dto(await selected, SkillSchemaRead)

@router.patch("/{skill_id}")
async def update_skill(data: SkillSchemaPatch, request: Request, skill_id: UUID7, crud: SkillCRUD = Depends()):
    info = data.model_dump(exclude_unset=True)
    updated = crud.update(
        Skill.user_id == get_user_id_by_session(request), 
        Skill.id == skill_id, 
        **info)
    return model_to_dto(await updated, SkillSchemaRead)

@router.delete("/{skill_id}")
async def delete_skill(skill_id: UUID7, request: Request, crud: SkillCRUD = Depends()):
    deleted = crud.delete(
        Skill.user_id == get_user_id_by_session(request), 
        Skill.id == skill_id)
    return model_to_dto(await deleted, SkillSchemaRead)