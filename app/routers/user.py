import logging
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
import app.models as models
from app.schemas import UserRegister
from app.utils import get_brazil_time
from app.services.security import create_verify_token_firebase
from app.schemas import TokenVerify
import datetime
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
        is_active=False,
        roles={},
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    verify_token = create_verify_token_firebase({'email': new_user.email, 'is_active': new_user.is_active})
    print('Enviar primeiro e-mail, Mensagem de Sucesso e e-mail enviado')
    return verify_token

@router.post('/activate')
def activate_user(token: TokenVerify, db: Session = Depends(get_db)):
    if token.expire < get_brazil_time() and token.is_active == False:
        print('Enviar e-mail de validação')
        raise HTTPException(status_code=400, detail='Verifique seu e-mail para validação')
        
    user = models.User.find_by_email(db=db, email=token.email)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    user.is_active = True
    user.activated_at = get_brazil_time()
    db.commit()
    db.refresh(user)
    return {'message': 'User activated successfully'}

@router.post('/login')
def login_user():
    pass

@router.post('/logout')
def logout_user():
    pass
@router.delete('/delete')
def delete_user():
    pass
@router.put('/update')
def update_user():
    pass


