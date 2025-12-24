from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.schemas import ItemSchemaCreate

router = APIRouter(prefix="/item")

@router.get("")
def get_all_items(limit: int = 20, offset: int = 0):
    pass

@router.post("")
def create_item():
    pass

@router.get("/{item_id}")
def get_item(item_id: UUID7):
    pass

@router.patch("/{item_id}")
def update_item(item_id: UUID7):
    pass

@router.delete("/{item_id}")
def delete_item(item_id: UUID7):
    pass
