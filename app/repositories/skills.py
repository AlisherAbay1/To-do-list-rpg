from app.core import database
from sqlalchemy import select, update
from app.models import Skill as SkillModel
from app.schemas import SkillSchemaRead

def get_all_skills_rep():
    with database.LocalSession.begin() as session:
        skills = session.scalars(select(SkillModel)).all()
        return [SkillSchemaRead.model_validate(skill).model_dump() for skill in skills]

def get_skill_by_id_rep(id):
    with database.LocalSession.begin() as session:
        skill = session.scalar(select(SkillModel).where(SkillModel.id == id))
        return SkillSchemaRead.model_validate(skill).model_dump()

def create_skill_rep(skill_info):
    with database.LocalSession.begin() as session:
        skill = SkillModel(**skill_info.model_dump())
        session.add(skill)
        return {"response": "Successfully created"}
    
def update_skill_rep(id, skill_info):
    with database.LocalSession.begin() as session:
        session.execute(update(SkillModel).where(SkillModel.id == id).values(**skill_info.model_dump()))
        return {"response": "Successfully update"}
    
def delete_skill_rep(id):
    with database.LocalSession.begin() as session:
        skill = session.scalar(select(SkillModel).where(SkillModel.id == id))
        session.delete(skill)
        return {"response": "Successfully delete"}