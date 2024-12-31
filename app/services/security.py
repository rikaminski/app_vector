from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth

from app.utils import get_brazil_time
import jwt
from datetime import timedelta
from firebase_admin import credentials
import firebase_admin

cred = credentials.Certificate("/home/ostuff/Desktop/auth_app_vector/sample-firebase-ai-app-39af5-firebase-adminsdk-tk69o-702271570f.json")
firebase_admin.initialize_app(cred)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_verify_token(data: dict):
    to_encode = data.copy()
    expire = get_brazil_time() + timedelta(minutes=10)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, 'secret', algorithm='HS256')
    return {
        'token': encoded_jwt,
        'expire': expire.isoformat(),
        'email': data['email'],
        'is_active': data['is_active'],
        'token_type': 'bearer'
    }

def create_verify_token_firebase(data: dict):
    to_encode = data.copy()
    expire = get_brazil_time() + timedelta(minutes=10)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, 'secret', algorithm='HS256')
    
    # Create a custom token with Firebase
    firebase_token = auth.create_custom_token(data['email'])
    
    return {
        'token': encoded_jwt,
        'firebase_token': firebase_token.decode('utf-8'),
        'expire': expire.isoformat(),
        'email': data['email'],
        'is_active': data['is_active'],
        'token_type': 'bearer'
    }