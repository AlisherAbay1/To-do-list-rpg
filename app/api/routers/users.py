from fastapi import APIRouter, Response, Cookie
from pydantic import UUID7
from app.schemas import UserSchemaPatchEmail, UserSchemaRead, UserEmailDTO, \
                        UserSchemaPatchPassword, UserPasswordDTO, UserSchemaCreateAuth, \
                        CreateUserDTO, UserSchemaAuth, LoginIdentifierDTO
from app.repositories import UserRepository, RedisRepository, TransactionAlchemyManager
from fastapi import Depends, HTTPException
from app.services.interactors import GetUsersInteractor, UpdateCurrentUserEmailInteractor, DeleteCurrentUserInteractor, \
                                    GetUserInteractor, GetSessionTimeInteractor, UpdateCurrentUserPasswordInteractor, \
                                    CreateUserInteractor, GetCurrentUser, AuthenticateUserInteractor, \
                                    DeleteSessionInteractor, RefreshSessionTokenInteractor
from app.core.database import get_local_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis_config import MAX_AGE
from redis.asyncio import Redis
from app.core.redis_config import get_redis_session
from app.core.security import IS_PRODUCTION

router = APIRouter(prefix="/users")

@router.get("", response_model=list[UserSchemaRead])
async def get_all_users(limit: int = 20, 
                        offset: int = 0, 
                        session: AsyncSession = Depends(get_local_session)):
    repo = UserRepository(session)
    interactor = GetUsersInteractor(repo)
    return await interactor(limit, offset)

@router.get("/me", response_model=UserSchemaRead)
async def get_current_user(session_token = Cookie(None), 
                           session: AsyncSession = Depends(get_local_session), 
                           cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    interactor = GetCurrentUser(repo, cash_repo)
    return await interactor(session_token)

@router.post("/auth/registration")
async def create_user(response: Response, 
                      credentials: UserSchemaCreateAuth, 
                      session: AsyncSession = Depends(get_local_session),
                      cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    interactor = CreateUserInteractor(repo, cash_repo, transaction)
    dto = CreateUserDTO(
        username=credentials.username, 
        email=credentials.email, 
        password=credentials.password
    )
    user_result = await interactor(dto)

    response.set_cookie(key="session_token", 
                        value=user_result.session_token,
                        httponly=True,
                        max_age=MAX_AGE, 
                        samesite="lax",
                        secure=IS_PRODUCTION)
    
    return {"username": user_result.username, 
            "email": user_result.email, 
            "message": "User successfully created"}

@router.post("/auth/login")
async def sign_in_account(response: Response, 
                          credentials: UserSchemaAuth, 
                          session: AsyncSession = Depends(get_local_session),
                          cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = AuthenticateUserInteractor(repo, cash_repo)
    dto = LoginIdentifierDTO(
        username_or_email=credentials.username_or_email, 
        password=credentials.password
    )
    user_result = await interactor(dto)

    response.set_cookie(key="session_token", 
                        value=user_result.session_token,
                        httponly=True,
                        max_age=MAX_AGE, 
                        samesite="lax",
                        secure=IS_PRODUCTION)
    
    return {"username": user_result.username, 
            "email": user_result.email, 
            "message": "Successfully sign-in"}

@router.patch("/auth/get_session_time")
async def get_session_time(session_token: str = Cookie(None), 
                           cash_session: Redis = Depends(get_redis_session)):
    cash_repo = RedisRepository(cash_session)
    interactor = GetSessionTimeInteractor(cash_repo)
    return await interactor(session_token)

@router.patch("/auth/refresh")
async def refresh(session_token: str = Cookie(None),
                  cash_session: Redis = Depends(get_redis_session)):
    cash_repo = RedisRepository(cash_session)
    interactor = RefreshSessionTokenInteractor(cash_repo)
    return await interactor(session_token)

@router.delete("/auth/logout")
async def logout(response: Response, 
                 session_token = Cookie(None), 
                 cash_session: Redis = Depends(get_redis_session)):
    cash_repo = RedisRepository(cash_session)
    interactor = DeleteSessionInteractor(cash_repo)
    response.delete_cookie("session_token")
    if session_token:
        await interactor(session_token)
    return {"message": "Session is deleted"}

@router.patch("/me/email-change")
async def update_current_user_email(data: UserSchemaPatchEmail, 
                                    session_token = Cookie(None), 
                                    session: AsyncSession = Depends(get_local_session), 
                                    cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    interactor = UpdateCurrentUserEmailInteractor(repo, cash_repo, transaction)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserEmailDTO(new_email=data.new_email, password=data.password)
    new_email = await interactor(dto, session_token)
    return {
        "message": "Email updated successfully", 
        "new_email": new_email
    }

@router.patch("/me/password-change")
async def update_current_user_password(data: UserSchemaPatchPassword,
                                       session_token = Cookie(None), 
                                       session: AsyncSession = Depends(get_local_session),
                                       cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    interactor = UpdateCurrentUserPasswordInteractor(repo, cash_repo, transaction)
    dto = UserPasswordDTO(old_password=data.old_password, new_password=data.new_password)
    await interactor(dto, session_token)

    return {
        "message": "Password updated successfully"
    }

@router.delete("/me", status_code=204)
async def delete_current_user(session_token = Cookie(None), 
                              session: AsyncSession = Depends(get_local_session),
                              cash_session: Redis = Depends(get_redis_session)):
    repo = UserRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    
    interactor = DeleteCurrentUserInteractor(repo, cash_repo, transaction)
    await interactor(session_token)

@router.get("/{user_id}", response_model=UserSchemaRead)
async def get_user(user_id: UUID7, 
                   session: AsyncSession = Depends(get_local_session)):
    repo = UserRepository(session)
    interactor = GetUserInteractor(repo)
    return await interactor(user_id)
