from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import UUID7
from app.schemas import ItemSchemaCreate, ItemSchemaRead, ItemCreateDTO
from app.repositories import ItemRepository, RedisRepository, TransactionAlchemyManager
from app.services.interactors import GetAllItemsInteractor, GetCurrentUserItemsInteractor, CreateCurrentUserItemInteractor, \
                                    GetItemInteractor, DeleteItemInteractor
from app.core.database import get_local_session
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.core.redis_config import get_redis_session

router = APIRouter(prefix="/item")

@router.get("", response_model=list[ItemSchemaRead])
async def get_all_items(limit: int = 20, 
                        offset: int = 0, 
                        session: AsyncSession = Depends(get_local_session)):
    repo = ItemRepository(session)
    interactor = GetAllItemsInteractor(repo)
    return await interactor(limit, offset)

@router.get("/me", response_model=list[ItemSchemaRead])
async def get_current_user_items(request: Request, 
                                 limit: int = 20, 
                                 offset: int = 0, 
                                 session: AsyncSession = Depends(get_local_session), 
                                 cash_session: Redis = Depends(get_redis_session)):
    repo = ItemRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = GetCurrentUserItemsInteractor(repo, cash_repo)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_id, limit, offset)

@router.post("/me", response_model=ItemSchemaRead)
async def create_current_user_item(data: ItemSchemaCreate, 
                                   request: Request, 
                                   session: AsyncSession = Depends(get_local_session), 
                                   cash_session: Redis = Depends(get_redis_session)):
    repo = ItemRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    interactor = CreateCurrentUserItemInteractor(repo, cash_repo, transaction)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    dto = ItemCreateDTO(
        title=data.title, 
        description=data.description, 
        amount=data.amount
    )
    return await interactor(session_id, dto)

@router.get("/{item_id}", response_model=ItemSchemaRead)
async def get_item(item_id: UUID7, 
                   session: AsyncSession = Depends(get_local_session)):
    repo = ItemRepository(session)
    interactor = GetItemInteractor(repo)
    return await interactor(item_id)

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: UUID7,
                      session: AsyncSession = Depends(get_local_session)):
    repo = ItemRepository(session)
    transaction = TransactionAlchemyManager(session)
    interactor = DeleteItemInteractor(repo, transaction)
    return await interactor(item_id)
