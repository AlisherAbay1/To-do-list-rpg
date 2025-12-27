from app.services import get_user_by_session_services
from fastapi import HTTPException, Request
from app.core import redis_config

def get_user_by_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(401, "Not authenticated")
    user = get_user_by_session_services(session_id)
    if not user:
        raise HTTPException(401, "Invalid session")
    return user

def  get_user_id_by_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(401, "Not authenticated")
    username = redis_config.r.get(f"session:{session_id}")
    return username

def get_session_id(request: Request):
    return {"session_id": request.cookies.get("session_id")}