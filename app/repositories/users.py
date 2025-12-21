from app.core import LocalSession
from app.models.users import User as ModelUser
from sqlalchemy import select, update
from app.schemas import UserSchemaRead, TaskSchemaRead, SkillSchemaRead, ItemSchemaRead
from app.models import Task as ModelTask
from app.models import Skill as ModelSkill
from app.models import Item as ModelItem
from fastapi import HTTPException

def get_all_users_rep():
    with LocalSession.begin() as session:
        users = session.scalars(select(ModelUser)).all()
        return [UserSchemaRead.model_validate(user).model_dump() for user in users]

def get_all_usernames():
    with LocalSession.begin() as session:
        usernames = session.scalars(select(ModelUser.username))
        return usernames

def get_user_rep(id):
    with LocalSession.begin() as session:
        user = session.scalars(select(ModelUser).where(ModelUser.id == id)).first()
        return UserSchemaRead.model_validate(user).model_dump()

def get_tasks_by_user_id_rep(user_id):
    with LocalSession.begin() as session:
        tasks = session.scalars(select(ModelTask).where(ModelTask.user_id == user_id)).all()
        return [TaskSchemaRead.model_validate(task).model_dump() for task in tasks]

def get_skills_by_user_id_rep(user_id):
    with LocalSession.begin() as session:
        skills = session.scalars(select(ModelSkill).where(ModelSkill.user_id == user_id)).all()
        return [SkillSchemaRead.model_validate(skill).model_dump() for skill in skills]

def get_items_by_user_id_rep(user_id):
    with LocalSession.begin() as session:
        items = session.scalars(select(ModelItem).where(ModelItem.user_id == user_id))
        return [ItemSchemaRead.model_validate(item).model_dump() for item in items]

def create_user_rep(user_info):
    with LocalSession.begin() as session:
        user = ModelUser(**user_info.model_dump())
        session.add(user)
        return {"response": "Succesfully created"}

def update_user_rep(id, user_info):
    with LocalSession.begin() as session:
        statement = update(ModelUser).where(ModelUser.id == id).values(**user_info.model_dump())
        session.execute(statement)
        return {"response": "Succesfully updated"}
    
def delete_user_rep(id):
    with LocalSession.begin() as session:
        user = session.scalars(select(ModelUser).where(ModelUser.id == id)).first()
        session.delete(user)
        return {"response": "Succesfully deleted"}
    
def get_password_hash_by_username(username):
    with LocalSession.begin() as session:
        password_hash = session.scalar(
            select(ModelUser.password).where(ModelUser.username == username)
            )
        if password_hash == None:
            raise HTTPException(500, "Password isn't correct.")
        return password_hash