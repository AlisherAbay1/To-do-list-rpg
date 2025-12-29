from app.core.database import LocalSession
from app.models.users import User
from app.core.dto import model_to_dto
from app.schemas.users import UserSchemaRead
from sqlalchemy import insert

async def create_account_rep(credentials) -> UserSchemaRead:
    session = LocalSession()
    inserted = insert(User).values(**credentials.model_dump()).returning(User)
    obj = model_to_dto(await session.scalar(inserted), UserSchemaRead)
    await session.commit()
    return obj