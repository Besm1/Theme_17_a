from fastapi import APIRouter, HTTPException, Path
from typing import Annotated

router = APIRouter(prefix='/user',tags=['user'])
users = []

@router.get(path='/')
async def all_users():
    return users

@router.get(path='/user_id')
async def user_by_id(user_id:int):
    for u_ in users:
        if u_['id'] == user_id:
            return u_
    raise HTTPException(status_code=404, detail=f'User {user_id} not found.')

@router.post('/create/{username}/{firstname}/{lastname}/{age}')
async def create_user(username: Annotated[str, Path(...,min_length=5, max_length=20)],
                      firstname: Annotated[str, Path(...,min_length=2, max_length=20)],
                      lastname: Annotated[str, Path(...,min_length=2, max_length=20)],
                      age: Annotated[int, Path(..., ge=12, le=120)]):
    idx = (max([u_['id'] for u_ in users]) if users else 0) + 1
    users.append({'id': idx, 'username':username, 'firstname':firstname, 'lastname':lastname, 'age':age})
    return {"message":f"User {idx} successfully created."}

@router.put('/update/{user_id}/{username}/{firstname}/{lastname}/{age}')
async def update_user(user_id:int,
                      username: Annotated[str, Path(...,min_length=5, max_length=20)],
                      firstname: Annotated[str, Path(...,min_length=2, max_length=20)],
                      lastname: Annotated[str, Path(...,min_length=2, max_length=20)],
                      age: Annotated[int, Path(..., ge=12, le=120)]):
    for u_ in users:
        if u_['id'] == user_id:
            u_ = {'id': user_id, 'username':username, 'firstname':firstname, 'lastname':lastname, 'age':age}
            return {"message":f"User {user_id} successfully updated."}
    raise HTTPException(status_code=404, detail=f'User {user_id} not found.')

@router.delete('/delete/{user_id}')
async def delete_user (user_id:int):
    for i in range(len(users)):
        if users[i]['id'] == user_id:
            users.pop(i)
            return {"message":f"User {user_id} successfully deleted."}
    raise HTTPException(status_code=404, detail=f"User {user_id} not found.")
