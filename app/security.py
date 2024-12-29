from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
# from models import User
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(db: AsyncSession = Depends(get_db)):
    return None