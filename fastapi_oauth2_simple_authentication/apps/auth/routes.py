from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from db import get_db

from apps.user import db_queries
from apps.auth.hash_password import HashPassword

from . import oauth2


router = APIRouter(
    tags=['authentication'],
)


@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db_queries.get_user(db, username=request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not HashPassword.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')

    access_token = oauth2.create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
