from fastapi import APIRouter, Response, Cookie
from pydantic import UUID7
from src.app.presentation.schemas import UserSchemaPatchEmail, UserSchemaRead, UserSchemaPatchPassword, \
                                     UserSchemaCreateAuth, UserSchemaAuth
from src.app.application.dto.users import UserEmailDTO, CreateUserDTO, UserPasswordDTO, \
                                      LoginIdentifierDTO
from fastapi import HTTPException
from src.app.application.interactors import GetAllUsersInteractor, UpdateCurrentUserEmailInteractor, DeleteCurrentUserInteractor, \
                                        GetUserInteractor, GetSessionTimeInteractor, UpdateCurrentUserPasswordInteractor, \
                                        CreateUserInteractor, GetCurrentUser, AuthenticateUserInteractor, \
                                        DeleteSessionInteractor, RefreshSessionTokenInteractor
from src.app.core.redis_config import MAX_AGE
from src.app.core.security import IS_PRODUCTION
from dishka.integrations.fastapi import FromDishka, DishkaRoute

router = APIRouter(prefix="/users", route_class=DishkaRoute)

@router.get("", response_model=list[UserSchemaRead])
async def get_all_users(interactor: FromDishka[GetAllUsersInteractor], 
                        limit: int = 20, 
                        offset: int = 0):
    return await interactor(limit, offset)

@router.get("/me", response_model=UserSchemaRead)
async def get_current_user(interactor: FromDishka[GetCurrentUser], 
                           session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token)


@router.post("/auth/registration")
async def create_user(response: Response, 
                      credentials: UserSchemaCreateAuth, 
                      interactor: FromDishka[CreateUserInteractor]):
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
                          interactor: FromDishka[AuthenticateUserInteractor]): 
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
async def get_session_time(interactor: FromDishka[GetSessionTimeInteractor], 
                           session_token: str = Cookie(None)):
    return await interactor(session_token)

@router.patch("/auth/refresh")
async def refresh(interactor: FromDishka[RefreshSessionTokenInteractor], 
                  session_token: str = Cookie(None)):
    return await interactor(session_token)

@router.delete("/auth/logout")
async def logout(interactor: FromDishka[DeleteSessionInteractor], 
                 response: Response, 
                 session_token = Cookie(None)):
    response.delete_cookie("session_token")
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    await interactor(session_token)
    return {"message": "Session is deleted"}

@router.patch("/me/email-change")
async def update_current_user_email(interactor: FromDishka[UpdateCurrentUserEmailInteractor], 
                                    data: UserSchemaPatchEmail, 
                                    session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserEmailDTO(new_email=data.new_email, password=data.password)
    new_email = await interactor(dto, session_token)
    return {
        "message": "Email updated successfully", 
        "new_email": new_email
    }

@router.patch("/me/password-change")
async def update_current_user_password(interactor: FromDishka[UpdateCurrentUserPasswordInteractor], 
                                       data: UserSchemaPatchPassword,
                                       session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserPasswordDTO(old_password=data.old_password, new_password=data.new_password)
    await interactor(dto, session_token)

    return {
        "message": "Password updated successfully"
    }

@router.delete("/me", status_code=204)
async def delete_current_user(interactor: FromDishka[DeleteCurrentUserInteractor], 
                              session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    
    await interactor(session_token)

@router.get("/{user_id}", response_model=UserSchemaRead)
async def get_user(interactor: FromDishka[GetUserInteractor], 
                   user_id: UUID7):
    return await interactor(user_id)
