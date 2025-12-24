from fastapi import APIRouter, HTTPException, Response, Request
from app.schemas import UserSchemaCreateAuth, UserSchemaCreate
from app.repositories import auth
import app.services as services
from app.core import security
from app.core import redis_config
from app.services import create_session, delete_session, get_user_by_session_services

router = APIRouter(prefix="/auth")

def get_user_by_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(401, "Not authenticated")
    user = get_user_by_session_services(session_id)
    if not user:
        raise HTTPException(401, "Invalid session")
    return user

def get_session_id(request: Request):
    return {"session_id": request.cookies.get("session_id")}

@router.post("/registration")
def create_account(response: Response, credentials: UserSchemaCreateAuth):
    if services.does_exist_schema(credentials.username):
        raise HTTPException(409, "Username already taken.")
    
    account = auth.create_account_rep(UserSchemaCreate(
        username=credentials.username, 
        email=credentials.email, 
        password=security.hash_password(credentials.password)
        )
    )
    response.set_cookie(key="session_id", 
                            value=create_session(credentials.username),
                            httponly=True,
                            max_age=redis_config.MAX_AGE, 
                            samesite="lax",
                            secure=True)
    return account

@router.post("/login")
def sign_in_account(response: Response, credentials: UserSchemaCreateAuth):
    if services.sign_in_account(credentials):
        response.set_cookie(key="session_id", 
                            value=create_session(credentials.username),
                            httponly=True,
                            max_age=redis_config.MAX_AGE, 
                            samesite="lax",
                            secure=True)
        
        return {"response": "Successfully sign-in"}
    raise HTTPException(401, "Incorrect password")

@router.delete("/logout")
def logout(response: Response, request: Request):
    is_deleted = delete_session(request.cookies.get("session_id"))
    if is_deleted:
        response.delete_cookie("session_id")
        return {"response": "Session deleted."}
    return {"response": "Session already deleted."}

