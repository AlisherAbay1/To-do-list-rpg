from fastapi import APIRouter, HTTPException
from app.schemas import SkillSchemaCreate
from app.repositories.skills import create_skill_rep, get_skill_by_id_rep, get_all_skills_rep, update_skill_rep, delete_skill_rep
from pydantic import UUID7

router = APIRouter(prefix="/skill")

@router.get("")
def get_all_skills(limit: int = 20, offset: int = 0):
    pass

@router.post("")
def create_skill():
    pass

@router.get("/{skill_id}")
def get_skill(skill_id: UUID7):
    pass

@router.patch("/{skill_id}")
def update_skill(skill_id: UUID7):
    pass

@router.delete("/{skill_id}")
def delete_skill(skill_id: UUID7):
    pass

