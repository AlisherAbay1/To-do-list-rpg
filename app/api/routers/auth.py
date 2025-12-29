from fastapi import APIRouter, HTTPException, Response, Request, Depends
from app.schemas import UserSchemaCreateAuth, UserSchemaCreate, UserSchemaAuth
from app.repositories import auth
from app.services import does_exist_in_schema
from app.core.security import hash_password, password_verify
from app.core import redis_config
from app.services import create_session, delete_session, get_hashed_password_by_id
from app.repositories.users import UserCRUD

router = APIRouter(prefix="/auth")

@router.post("/registration")
async def create_account(response: Response, credentials: UserSchemaCreateAuth, crud: UserCRUD = Depends()):
    if does_exist_in_schema(crud._model.username == credentials.username):
        raise HTTPException(409, "Username already taken.")
    if does_exist_in_schema(crud._model.email == credentials.email):
        raise HTTPException(409, "Email already taken.")
    
    account = await auth.create_account_rep(UserSchemaCreate(
        username=credentials.username, 
        email=credentials.email, 
        password=hash_password(credentials.password)
        )
    )
    response.set_cookie(key="session_id", 
                            value=await create_session(str(account.id)),
                            httponly=True,
                            max_age=redis_config.MAX_AGE, 
                            samesite="lax",
                            secure=True)
    return account

@router.post("/login")
async def sign_in_account(response: Response, credentials: UserSchemaAuth):
    if password_verify(
        credentials.password, 
        await get_hashed_password_by_id(credentials.id)):
        response.set_cookie(key="session_id", 
                            value=await create_session(str(credentials.id)),
                            httponly=True,
                            max_age=redis_config.MAX_AGE, 
                            samesite="lax",
                            secure=True)
        return {"response": "Successfully sign-in"}
    raise HTTPException(401, "Incorrect username or password")

@router.delete("/logout")
async def logout(response: Response, request: Request):
    is_deleted = delete_session(request.cookies.get("session_id"))
    if is_deleted:
        response.delete_cookie("session_id")
        return {"response": "Session deleted."}
    raise HTTPException(410, "Session already deleted")