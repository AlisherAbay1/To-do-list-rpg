from fastapi import APIRouter, Cookie, HTTPException
from src.app.presentation.schemas import SkillSchemaCreate, SkillSchemaRead
from src.app.application.dto.skills import SkillCreateDTO
from pydantic import UUID7
from src.app.application.interactors import GetAllSkillsInteractor, GetCurrentUserSkillsInteractor, CreateCurrentUserSkillInteractor, \
                                    GetSkillInteractor, DeleteSkillInteractor
from dishka.integrations.fastapi import FromDishka, DishkaRoute

router = APIRouter(prefix="/skill", route_class=DishkaRoute)

@router.get("", response_model=list[SkillSchemaRead])
async def get_all_skills(interactor: FromDishka[GetAllSkillsInteractor], 
                         limit: int = 20, 
                         offset: int = 0):
    return await interactor(limit, offset)

@router.get("/me", response_model=list[SkillSchemaRead])
async def get_current_user_skills(interactor: FromDishka[GetCurrentUserSkillsInteractor], 
                                  session_token = Cookie(None), 
                                  limit: int = 20, 
                                  offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.post("/me", response_model=SkillSchemaRead)
async def create_current_user_skill(interactor: FromDishka[CreateCurrentUserSkillInteractor], 
                                    data: SkillSchemaCreate, 
                                    session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = SkillCreateDTO(
        title=data.title,
        description=data.description, 
        ico=data.ico, 
        lvl=data.lvl, 
        xp=data.xp
    )
    return await interactor(session_token, dto)

@router.get("/{skill_id}", response_model=SkillSchemaRead)
async def get_skill(skill_id: UUID7, 
                    interactor: FromDishka[GetSkillInteractor], ):
    return await interactor(skill_id)

@router.delete("/{skill_id}", status_code=204)
async def delete_skill(skill_id: UUID7, 
                       interactor: FromDishka[DeleteSkillInteractor]):
    await interactor(skill_id)
