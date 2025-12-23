from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.schemas.task import GetTaskOut, PostTaskIn, PostTaskOut, PutTaskIn, PutTaskOut, DeleteTaskOut
from api.cruds.task import create_task, get_tasks, update_task, delete_task
from api.utils.auth import get_current_user
from api.models.users import Users


router = APIRouter()


@router.post("/api/tasks", response_model=PostTaskOut)
def create_task_endpoint(
    task_in: PostTaskIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_task(db, task_in, current_user)


@router.get("/api/tasks", response_model=List[GetTaskOut])
def get_tasks_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    print("get_tasks_endpoint")
    return get_tasks(db, current_user)

@router.put("/api/tasks/{task_id}", response_model=PutTaskOut)
def update_task_endpoint(
    task_id: int,
    task_in: PutTaskIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_task(db, task_id, task_in, current_user)


@router.delete("/api/tasks/{task_id}", response_model=DeleteTaskOut)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_task(db, task_id, current_user)
