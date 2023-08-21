from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from typing import Annotated

from . import db_queries, schemas
from db import get_db

from auth import authenticate_user


router = APIRouter(prefix='/users', tags=['User'])


@router.get('/protected/')
async def protected(credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_user)]):
    return {'message': 'protected route'}


@router.get('/', response_model=list[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db_queries.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db_queries.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_queries.create_user(db=db, user=user)


@router.delete('/', response_model=schemas.User)
async def delete_user(credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_user)], user: schemas.UserDelete, db: Session = Depends(get_db)):
    db_user = db_queries.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.delete_user(db=db, user=credentials)


@router.put('/{user_id}', response_model=schemas.User)
async def update_user(credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_user)], user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db_queries.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.update_user(db=db, user=user, user_id=user_id)
