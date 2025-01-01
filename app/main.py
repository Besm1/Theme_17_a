from fastapi import FastAPI
from .routers import task, user

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

@app.get('/')
async def main():
    return {'message': 'Welcome to TaskManager'}

app.include_router(task.router)
app.include_router(user.router)

