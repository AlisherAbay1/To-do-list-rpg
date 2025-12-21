from app.core import database
from sqlalchemy import select, update
from app.models import Item as ModelItem
from app.schemas import ItemSchemaRead

def create_item_rep(item_info):
    with database.LocalSession.begin() as session:
        item = ModelItem(**item_info.model_dump())
        session.add(item)
        return {"response": "Successfully created"}

def get_item_by_id_rep(id):
    with database.LocalSession.begin() as session:
        item = session.scalar(select(ModelItem).where(ModelItem.id == id))
        return ItemSchemaRead.model_validate(item).model_dump()

def get_all_items_rep():
    with database.LocalSession.begin() as session:
        items = session.scalars(select(ModelItem)).all()
        return [ItemSchemaRead.model_validate(item).model_dump() for item in items]

def update_item_rep(id, item_info):
    with database.LocalSession.begin() as session:
        session.execute(update(ModelItem).where(ModelItem.id == id).values(**item_info.model_dump()))
        return {"response": "Successfully updated"}
    
def delete_item_rep(id):
    with database.LocalSession.begin() as session:
        item = session.scalar(select(ModelItem).where(ModelItem.id == id))
        session.delete(item)
        return {"response": "Successfully deleted"}