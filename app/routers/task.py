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

@router.get(path='/all_tasks/{user_id}')
async def all_tasks(db: Annotated[Session, Depends(get_db)], user_id:int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@router.get(path='/task_id/{user_id}/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], user_id:int, task_id:int):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).one()
        if task:
            return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Task {task_id} for user {user_id} not found: {e}.')

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], new_task: CreateTask):
    db.execute(insert(Task).values(title=new_task.title,
                                          content=new_task.content,
                                          priority=new_task.priority,
                                          completed=False,
                                          user_id=new_task.user_id,
                                          slug=slugify(text=new_task.title)
                                          ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': f'Task for user {new_task.user_id} creation successful' }

@router.put('/update')
async def update_task():
    pass

@router.delete('/delete')
async def delete_task():
    pass
