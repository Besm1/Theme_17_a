from pydantic import BaseModel

class CreateUser(BaseModel):
    username:str
    firstname:str
    lastname:str
    age:int

    # class Config:
    #     orm_mode = True

class UpdateUser(BaseModel):
    firstname:str
    lastname:str
    age:int

    # class Config:
    #     orm_mode = True

class CreateTask(BaseModel):
    title:str
    content:str
    priority:int
    user_id:int

    # class Config:
    #     orm_mode = True

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id:int

    # class Config:
    #     orm_mode = True
