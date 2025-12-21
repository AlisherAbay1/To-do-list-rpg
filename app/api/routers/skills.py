from fastapi import APIRouter, HTTPException
from app.schemas import SkillSchemaCreate
from app.repositories.skills import create_skill_rep, get_skill_by_id_rep, get_all_skills_rep, update_skill_rep, delete_skill_rep
from pydantic import UUID7

router = APIRouter(prefix="/skill")

@router.get("/all")
def get_all_skills():
    try:
        return get_all_skills_rep()
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.get("/{id}")
def get_skill_by_id(id: UUID7):
    try:
        return get_skill_by_id_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.post("/")
def create_skill(skill_info: SkillSchemaCreate):
    try: 
        return create_skill_rep(skill_info)
    except Exception as e:
        raise HTTPException(500, detail=f'{e}')
    
@router.put("/{id}")
def update_skill(id: UUID7, skill_info: SkillSchemaCreate):
    try: 
        return update_skill_rep(id, skill_info)
    except Exception as e:
        raise HTTPException(500, detail=f'{e}')
    
@router.delete("/{id}")
def delete_skill(id: UUID7):
    try: 
        return delete_skill_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f'{e}')