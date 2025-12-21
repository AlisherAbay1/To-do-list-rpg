from app.core.database import LocalSession
from app.models.users import User
from app.schemas import UserSchemaRead
from sqlalchemy import select

def create_account_rep(credentials):
    with LocalSession.begin() as session:
        user = User(**credentials.model_dump())
        session.add(user)
        return {"response": "Successfully created"}
    
def get_pydantic_user_object(username):
    with LocalSession.begin() as session:
        user_obj = session.scalar(select(User).where(User.username == username))
        return UserSchemaRead.model_validate(user_obj)