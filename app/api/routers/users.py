from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.schemas import UserSchemaCreate
from app.repositories.users import create_user_rep, get_user_rep, update_user_rep, get_all_users_rep, delete_user_rep, get_tasks_by_user_id_rep, get_skills_by_user_id_rep, get_items_by_user_id_rep

router = APIRouter(prefix="/user")

@router.get("/all")
def get_all_users():
    try: 
        return get_all_users_rep()
    except Exception as e:
        raise HTTPException(500, detail=f"0{e}")

@router.get("/{id}")
def get_user(id: UUID7):
    try:
        return get_user_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.get("/{user_id}/tasks")
def get_tasks_by_user_id(user_id: UUID7):
    try:
        return get_tasks_by_user_id_rep(user_id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.get("/{user_id}/skills")
def get_skills_by_user_id(user_id: UUID7):
    try:
        return get_skills_by_user_id_rep(user_id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.get("/{user_id}/items")
def get_items_by_user_id(user_id: UUID7):
    try:
        return get_items_by_user_id_rep(user_id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

"""
admin access 
@router.post("/create")
def create_user(user_info: UserSchemaCreate):
    try:
        return create_user_rep(user_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")
"""

@router.put("/{id}")
def update_user(id: UUID7, user_info: UserSchemaCreate):
    try: 
        return update_user_rep(id, user_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")
    
@router.delete("/{id}")
def delete_user(id):
    try:
        return delete_user_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")