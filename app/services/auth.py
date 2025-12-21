from app.models import User
from app.core import LocalSession, security
from sqlalchemy import select, exists
from app.repositories import users

def does_exist_schema(username: str):
    with LocalSession.begin() as session:
        does_exist = session.execute(
            select(
                exists().where(User.username == username)
                )
            ).scalar()
    if does_exist:
        return True
    return False

def sign_in_account(credentials):
    if security.password_verify(credentials.password, users.get_password_hash_by_username(credentials.username)):
        return True
    return False 
