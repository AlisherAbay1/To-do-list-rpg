from fastapi import APIRouter, HTTPException
from app.repositories.tasks import get_all_tasks_rep, get_task_rep, create_tasks_rep, delete_task_rep, update_task_rep
from pydantic import UUID7
from app.schemas import TaskSchemaCreate

router = APIRouter(prefix="/task")

@router.get("/all")
def get_all_tasks():
    try: 
        return get_all_tasks_rep()
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.get("/{id}")
def get_user(id: UUID7):
    try: 
        return get_task_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.post("/create")
def create_task(task_info: TaskSchemaCreate):
    try: 
        return create_tasks_rep(task_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.put("/{id}")
def update_task(id: UUID7, task_info: TaskSchemaCreate):
    try: 
        return update_task_rep(id, task_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.delete("/{id}")
def delete_task(id: UUID7):
    try: 
        return delete_task_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")