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

from app.utils import _get_user_by_id

router = APIRouter(prefix='/task',tags=['task'])

@router.get(path='/all_tasks')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get(path='/task_id/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], user_id:int, task_id:int):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id)).one()
        if task:
            return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Task {task_id} for user {user_id} not found: {e}.')

@router.post('/create/{user_id}')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id:str,  new_task: CreateTask):
    try:
        user = await _get_user_by_id(db, user_id)
        if user:
            db.execute(insert(Task).values(title=new_task.title,
                                              content=new_task.content,
                                              priority=new_task.priority,
                                              completed=False,
                                              user_id=user.id,
                                              slug=slugify(text=new_task.title)
                                              ))
            db.commit()
            return {'status_code': status.HTTP_201_CREATED,
                    'transaction': f'Task for user \"{user.username}\" (Id={user.id}) creation successful' }
        else:
            return{'status_code': status.HTTP_400_BAD_REQUEST,
                    'transaction': f'User {user_id} not found'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Exception  occurred, details:"{e}"')


@router.put('/update/{task_id}')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, upd_task:UpdateTask):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id)).one()
        db.execute(update(Task).where(Task.id == task_id).values(title=upd_task.title,
                                          content=upd_task.content,
                                          priority=upd_task.priority,
                                          completed=upd_task.completed))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': f'Task {task.id} update successful' }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Exception  occurred while trying task update, details:"{e}"')


@router.delete('/delete/{task_id}')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id)).one()
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': f'Task {task_id} successfully deleted.' }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Exception  occurred while trying task update, details:"{e}"')
