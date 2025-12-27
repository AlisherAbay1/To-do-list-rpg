from uuid import uuid4
from app.core import redis_config
from fastapi import HTTPException
from app.repositories.users import UserCRUD
from app.models.users import User

def create_session(username):
    session_id = str(uuid4())
    redis_config.r.setex(f"session:{session_id}", redis_config.MAX_AGE, username)
    return session_id

def delete_session(session_id):
    is_deleted = redis_config.r.delete(f"session:{session_id}")
    if is_deleted:
        return True
    return False
    
def get_user_by_session_services(session_id):
    user = UserCRUD()
    username = redis_config.r.get(f"session:{session_id}")
    if username:
        return user.select(User.username == username)
    raise HTTPException(400, "Session expired.")