from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.schemas import UserSchemaCreate, UserSchemaPatch, UserSchemaRead
from app.repositories.users import UserCRUD
from fastapi import Depends, Request
from app.core.session import get_user_by_session, get_user_id_by_session
from app.core.dto import model_to_dto, models_to_dtos
from app.models.users import User

router = APIRouter(prefix="/users")

@router.get("")
def get_all_users(limit: int = 20, offset: int = 0, crud: UserCRUD = Depends()):
    return models_to_dtos(crud.select_many(limit, offset), UserSchemaRead)

@router.get("/me")
def get_current_user(request: Request):
    return model_to_dto(get_user_by_session(request), UserSchemaRead)

@router.patch("/me")
def update_current_user(data: UserSchemaCreate, request: Request, crud: UserCRUD = Depends()):
    updated = crud.update(User.id == get_user_id_by_session(request), **data.model_dump())
    return model_to_dto(updated, UserSchemaRead)

@router.delete("/me")
def delete_current_user(request: Request, crud: UserCRUD = Depends()):
    deleted = crud.delete(User.id == get_user_id_by_session(request))
    return model_to_dto(deleted, UserSchemaRead)

# admin
@router.get("/{user_id}")
def get_user(user_id: UUID7, crud: UserCRUD = Depends()):
    selected = crud.select(User.id == user_id)
    return model_to_dto(selected, UserSchemaRead)

# admin
@router.patch("/{user_id}")
def update_user(user_id: UUID7, data: UserSchemaPatch, crud: UserCRUD = Depends()):
    updated = crud.update(User.id == user_id, **data.model_dump(exclude_unset=True))
    return model_to_dto(updated, UserSchemaRead) 

# admin
@router.delete("/{user_id}")
def delete_user(user_id: UUID7, crud: UserCRUD = Depends()):
    deleted = crud.delete(User.id == user_id)
    return model_to_dto(deleted, UserSchemaRead)