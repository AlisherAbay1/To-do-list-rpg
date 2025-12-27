from app.core.database import LocalSession
from app.models.users import User

def create_account_rep(credentials):
    with LocalSession.begin() as session:
        user = User(**credentials.model_dump())
        session.add(user)
        return {"response": "Successfully created"}
