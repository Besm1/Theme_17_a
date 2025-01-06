from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models import User


async def _get_user_by_id(db:Annotated[Session, Depends(get_db)], user_id:str) -> User:
    return (db.scalars(select(User).where(User.id == int(user_id))).one() if user_id.isnumeric()
        else db.scalars(select(User).where(User.username == user_id)).one())

