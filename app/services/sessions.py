from uuid import uuid4
from app.core import redis_config
from fastapi import HTTPException
from sqlalchemy import select
from app.models.users import User
from app.schemas.users import UserSchemaRead
from app.core.database import LocalSession
from app.core.dto import model_to_dto

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
    async with LocalSession.begin() as session:
        id = await redis_config.r.get(f"session:{session_id}")
        user = session.scalar(select(User).where(User.id == id))
        if id:
            return model_to_dto(await user, UserSchemaRead)
        raise HTTPException(400, "Session expired.")