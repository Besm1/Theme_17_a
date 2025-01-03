from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Path
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user',tags=['user'])

async def _get_user_by_id(db:Annotated[Session, Depends(get_db)], user_id:str) -> User:
    return (db.scalars(select(User).where(User.id == int(user_id))).one() if user_id.isnumeric()
        else db.scalars(select(User).where(User.username == user_id)).one())


@router.get(path='/all_users')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get(path='/user_id/{user_id}')
async def user_by_id(db:Annotated[Session, Depends(get_db)], user_id:str):
    try:
        return await _get_user_by_id(db, user_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found.')

@router.post('/create')
async def create_user(db:Annotated[Session, Depends(get_db)], new_user:CreateUser):
    db.execute(insert(User).values(username=new_user.username
                                   , firstname=new_user.firstname
                                   , lastname=new_user.lastname
                                   , age=new_user.age
                                   , slug=slugify(text=new_user.username)
                                   ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful' }

@router.put('/update/{user_id}')
async def update_user(db:Annotated[Session, Depends(get_db)], user_id:str, upd_user:UpdateUser ):
    try:
        user = await _get_user_by_id(db, user_id)
        if user:
            db.execute(update(User).where(User.id == user.id).values(firstname=upd_user.firstname
                                                                     , lastname=upd_user.lastname
                                                                     , age=upd_user.age
                                                                     ))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'Successful user update.' }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found.')

@router.delete('/delete/{user_id}')
async def delete_user (db:Annotated[Session, Depends(get_db)], user_id:str):
    try:
        user = await _get_user_by_id(db, user_id)
        if user:
            db.execute(delete(User).where(User.id == user.id))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'Successful user delete.' }
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found.")
