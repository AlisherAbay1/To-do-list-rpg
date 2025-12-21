from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.repositories.items import create_item_rep, get_item_by_id_rep, update_item_rep, delete_item_rep, get_all_items_rep
from app.schemas import ItemSchemaCreate

router = APIRouter(prefix="/item")

@router.get("/all")
def get_all_items():
    try:
        return get_all_items_rep()
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")

@router.post("/{id}")
def create_item(item_info: ItemSchemaCreate):
    try:
        return create_item_rep(item_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")
    
@router.get("/{id}")
def get_item_by_id(id: UUID7):
    try:
        return get_item_by_id_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")
    
@router.put("/{id}")
def update_item(id: UUID7, item_info: ItemSchemaCreate):
    try:
        return update_item_rep(id, item_info)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")
    
@router.delete("/{id}")
def delete_item(id: UUID7):
    try:
        return delete_item_rep(id)
    except Exception as e:
        raise HTTPException(500, detail=f"{e}")