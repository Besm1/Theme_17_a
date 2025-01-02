from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Path
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from app.models.task import Task
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix='/task',tags=['task'])

@router.get(path='/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get(path='/task_id/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id:int):
    task = db.scalars(select(Task).where(Task.id == task_id)).all()
    if task:
        return task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found.')

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], new_task: CreateTask):
    task = db.scalars(insert(Task).values(title=new_task.title,
                                          content=new_task.content,
                                          priority=new_task.priority,
                                          completed=False,
                                          user_id=new_task.user_id,
                                          ))

@router.put('/update')
async def update_task():
    pass

@router.delete('/delete')
async def delete_task():
    pass
