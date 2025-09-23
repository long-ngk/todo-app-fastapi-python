from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.models import Task, User
from app.schemas.task import Task as TaskSchema
from app.schemas.task import TaskCreate

router = APIRouter()


@router.post("/tasks/", response_model=TaskSchema)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = Task(**task.model_dump(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks/", response_model=List[TaskSchema])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    setattr(task, 'status', status)
    db.commit()
    return {"message": "Task status updated successfully"}


@router.patch("/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    setattr(task, 'is_completed', True)
    db.commit()
    return {"message": "Task completed successfully"}
