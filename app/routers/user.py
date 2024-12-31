import logging
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas import UserRegister
from app.security import get_current_user
from app.utils import get_brazil_time

router = APIRouter(prefix='/user', tags=['user'])

#CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/register')
def create_user(user_data: UserRegister, db: Session = Depends(get_db)):

    existing_user = models.User.find_by_email(db=db,email= user_data.email)
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')
    
    if existing_user:
        logging.info(f"Email {user_data.email} is already registered")
        raise HTTPException(status_code=400, detail='Email already registered')
    
    new_user = models.User(
        uuid=uuid.uuid4(),
        name=user_data.name,
        nickname=user_data.nickname,
        email=user_data.email,
        hashed_password=user_data.password,  # Hash password before
        created_at=get_brazil_time(),
        updated_at=get_brazil_time(),
        activated_at=None,
        is_active=True,
        roles={},
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
