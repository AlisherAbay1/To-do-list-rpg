from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import UUID7

from todo_rpg.application.dto import UserPasswordDTO
from todo_rpg.application.interactors import (
    AuthenticateUserInteractor,
    CreateUserInteractor,
    DeleteCurrentUserInteractor,
    DeleteSessionInteractor,
    GetAllUsersInteractor,
    GetCurrentUser,
    GetSessionTimeInteractor,
    GetUserInteractor,
    RefreshSessionTokenInteractor,
    UpdateCurrentUserEmailInteractor,
    UpdateCurrentUserPasswordInteractor,
    ChangeCurrentUserRankInteractor,
)
from todo_rpg.infrastructure.config import config
from todo_rpg.core.security import IS_PRODUCTION
from todo_rpg.presentation.mappers import UserSchemaMapper
from todo_rpg.presentation.schemas import (
    MessageSchema,
    UserNewEmailSchema,
    UserSchemaCreateAuth,
    UserSchemaPatchEmail,
    UserSchemaPatchPassword,
    UserSchemaRead,
    UserSignInSchema,
    UserSuccessAuthSchema,
)

router = APIRouter(prefix="/users", route_class=DishkaRoute)


@router.get("", response_model=list[UserSchemaRead])
async def get_all_users(
    interactor: FromDishka[GetAllUsersInteractor], limit: int = 20, offset: int = 0
):
    return await interactor(limit, offset)


@router.get("/me", response_model=UserSchemaRead)
async def get_current_user(
    interactor: FromDishka[GetCurrentUser], session_token=Cookie(None)
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token)


@router.get("/{user_id}", response_model=UserSchemaRead)
async def get_user(interactor: FromDishka[GetUserInteractor], user_id: UUID7):
    return await interactor(user_id)


@router.post("/auth/registration", response_model=UserSuccessAuthSchema)
async def create_user(
    response: Response,
    credentials: UserSchemaCreateAuth,
    interactor: FromDishka[CreateUserInteractor],
):
    dto = UserSchemaMapper.to_create_dto(credentials)
    user_result = await interactor(dto)

    response.set_cookie(
        key="session_token",
        value=user_result.session_token,
        httponly=True,
        max_age=config.redis.max_age,
        samesite="lax",
        secure=IS_PRODUCTION,
    )

    return UserSuccessAuthSchema(
        username=user_result.username,
        email=user_result.email,
        message="User successfully created",
    )


@router.post("/auth/login", response_model=UserSuccessAuthSchema)
async def sign_in_account(
    response: Response,
    credentials: UserSignInSchema,
    interactor: FromDishka[AuthenticateUserInteractor],
):
    dto = UserSchemaMapper.to_sign_in_dto(credentials)
    user_result = await interactor(dto)

    response.set_cookie(
        key="session_token",
        value=user_result.session_token,
        httponly=True,
        max_age=config.redis.max_age,
        samesite="lax",
        secure=IS_PRODUCTION,
    )

    return UserSuccessAuthSchema(
        username=user_result.username,
        email=user_result.email,
        message="Successfully sign-in",
    )


@router.patch("/auth/get_session_time", response_model=MessageSchema)
async def get_session_time(
    interactor: FromDishka[GetSessionTimeInteractor], session_token: str = Cookie(None)
):
    return await interactor(session_token)


@router.patch("/auth/refresh", response_model=MessageSchema)
async def refresh(
    interactor: FromDishka[RefreshSessionTokenInteractor],
    session_token: str = Cookie(None),
):
    return await interactor(session_token)


@router.delete("/auth/logout")
async def logout(
    interactor: FromDishka[DeleteSessionInteractor],
    response: Response,
    session_token=Cookie(None),
):
    response.delete_cookie("session_token")
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    await interactor(session_token)
    return MessageSchema(message="Session is deleted")


@router.patch("/me/email-change")
async def update_current_user_email(
    interactor: FromDishka[UpdateCurrentUserEmailInteractor],
    data: UserSchemaPatchEmail,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserSchemaMapper.to_email_dto(data)
    new_email = await interactor(dto, session_token)
    return UserNewEmailSchema(new_email=new_email, message="Email updated successfully")


@router.patch("/me/password-change")
async def update_current_user_password(
    interactor: FromDishka[UpdateCurrentUserPasswordInteractor],
    data: UserSchemaPatchPassword,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = UserPasswordDTO(
        old_password=data.old_password, new_password=data.new_password
    )
    await interactor(dto, session_token)

    return MessageSchema(message="Password updated successfully")


@router.delete("/me", status_code=204)
async def delete_current_user(
    interactor: FromDishka[DeleteCurrentUserInteractor], session_token=Cookie(None)
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")

    await interactor(session_token)


@router.get("/me/change-rank/")
async def change_rank(
    interactor: FromDishka[ChangeCurrentUserRankInteractor],
    rank_id: UUID7,
    session_token=Cookie(None),
):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")

    user_rank_title = await interactor(session_token, rank_id)

    return {"message": f"Your new rank is {user_rank_title}"}
