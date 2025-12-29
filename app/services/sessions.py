from uuid import uuid4
from app.core import redis_config
from fastapi import HTTPException
from app.repositories.users import UserCRUD
from app.models.users import User

async def create_session(username):
    session_id = str(uuid4())
    await redis_config.r.setex(f"session:{session_id}", redis_config.MAX_AGE, username)
    return session_id

async def delete_session(session_id):
    is_deleted = await redis_config.r.delete(f"session:{session_id}")
    if is_deleted:
        return True
    return False
    
async def get_user_by_session_services(session_id):
    user = UserCRUD()
    username = await redis_config.r.get(f"session:{session_id}")
    if username:
        return await user.select(User.username == username)
    raise HTTPException(400, "Session expired.")