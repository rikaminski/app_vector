import os
import sys

sys.path.insert(0, os.path.abspath(os.curdir))


import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas import UserRegister
from app.security import get_current_user
from app.utils import get_brazil_time

router = APIRouter(prefix='/user', tags=['user'])


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post('/register')
async def create_user(user_data: UserRegister, db: AsyncSessionDep):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')

    new_user = User(
        uuid=uuid.uuid4(),
        name=user_data.name,
        nickname=user_data.nickname,
        email=user_data.email,
        hashed_password=user_data.password,  # Hash password before
        created_at=get_brazil_time(),
        updated_at=get_brazil_time(),
        activated_at=get_brazil_time(),
        is_active=True,
        roles={},
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
