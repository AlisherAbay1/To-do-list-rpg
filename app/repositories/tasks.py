from app.core import database
from app.models.tasks import Task as ModelTask
from app.schemas.tasks import TaskSchemaRead
from sqlalchemy import select, update

def get_all_tasks_rep():
    with database.LocalSession.begin() as session:
        tasks = session.scalars(select(ModelTask)).all()
        return [TaskSchemaRead.model_validate(task).model_dump() for task in tasks]

def get_task_rep(id):
    with database.LocalSession.begin() as session:
        task = session.scalar(select(ModelTask).where(ModelTask.id == id))
        return TaskSchemaRead.model_validate(task).model_dump()
    
def create_tasks_rep(task_info):
    with database.LocalSession.begin() as session:
        task = ModelTask(**task_info.model_dump())
        session.add(task)
        return  {"response": "Succesfully created"}
    
def update_task_rep(id, task_info):
    with database.LocalSession.begin() as session:
        session.execute(update(ModelTask).where(ModelTask.id == id).values(**task_info.model_dump()))
        return {"response": "Succesfully updated"}

def delete_task_rep(id):
    with database.LocalSession.begin() as session:
        task = session.scalar(select(ModelTask).where(ModelTask.id == id))
        session.delete(task)
        return {"response": "Succesfully deleted"}