from fastapi import APIRouter, Depends, Request, HTTPException
from app.schemas import SkillSchemaCreate, SkillSchemaRead, SkillCreateOrUpdateDTO
from pydantic import UUID7
from app.repositories import SkillRepository, RedisRepository
from app.core.database import get_local_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.interactors import GetAllSkillsInteractor, GetCurrentUserSkillsInteractor, CreateCurrentUserSkillInteractor, \
                                    GetSkillInteractor, DeleteSkillInteractor
from redis.asyncio import Redis
from app.core.redis_config import get_redis_session

router = APIRouter(prefix="/skill")

@router.get("", response_model=list[SkillSchemaRead])
async def get_all_skills(limit: int = 20, 
                         offset: int = 0, 
                         session: AsyncSession = Depends(get_local_session)):
    repo = SkillRepository(session)
    interactor = GetAllSkillsInteractor(repo)
    return await interactor(limit, offset)

@router.get("/me", response_model=SkillSchemaRead)
async def get_current_user_skills(request: Request, 
                                  limit: int = 20, 
                                  offset: int = 0, 
                                  session: AsyncSession = Depends(get_local_session), 
                                  cash_session: Redis = Depends(get_redis_session)):
    repo = SkillRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = GetCurrentUserSkillsInteractor(repo, cash_repo)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_id, limit, offset)

@router.post("/me", response_model=SkillSchemaRead)
async def create_current_user_skill(data: SkillSchemaCreate, 
                                    request: Request, 
                                    session: AsyncSession = Depends(get_local_session), 
                                    cash_session: Redis = Depends(get_redis_session)):
    repo = SkillRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = CreateCurrentUserSkillInteractor(repo, cash_repo)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    dto = SkillCreateOrUpdateDTO(
        title=data.title,
        description=data.description, 
        ico=data.ico, 
        lvl=data.lvl, 
        xp=data.xp
    )
    return await interactor(session_id, dto)

@router.get("/{skill_id}", response_model=SkillSchemaRead)
async def get_skill(skill_id: UUID7, 
                    session: AsyncSession = Depends(get_local_session)):
    repo = SkillRepository(session)
    interactor = GetSkillInteractor(repo)
    return await interactor(skill_id)

@router.delete("/{skill_id}", status_code=204)
async def delete_skill(skill_id: UUID7, 
                       session: AsyncSession = Depends(get_local_session)):
    repo = SkillRepository(session)
    interactor = DeleteSkillInteractor(repo)
    return await interactor(skill_id)
