from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegister(BaseModel):
    name: str = Field(..., example='John Doe')
    nickname: str = Field(..., example='johnd')
    email: EmailStr = Field(..., example='johndoe@example.com')
    password: str = Field(..., example='password123')
    confirm_password: str = Field(..., example='password123')

class TokenVerify(BaseModel):
    token: str
    expire: datetime
    email: EmailStr
    token_type: str
    is_active: bool