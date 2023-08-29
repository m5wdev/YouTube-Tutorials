from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from db import get_db

from . import schemas, db_queries


router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/get-all', response_model=List[schemas.UserDetails])
async def get_all_users(db: Session = Depends(get_db)):
    return db_queries.get_all_users(db)


@router.get('/{id}', response_model=schemas.UserDetails)
async def get_user(id: int = None, email: str = None, db: Session = Depends(get_db)):
    user = db_queries.get_user(db, id, email)
    if not user:
        raise HTTPException(status_code=404, detail='There is no user in db with such credentials')
    return user


@router.post('/create', response_model=schemas.User)
async def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return db_queries.create_user(db, request)


@router.put('/{id}/update', response_model=schemas.UserDetails)
async def update_user(id: int, request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db_queries.update_user(db, user=request, user_id=id)
    if not user:
        raise HTTPException(status_code=400, detail='There is no user in db with such credentials')
    return user


@router.delete('/{id}/delete', response_model=schemas.User)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db_queries.get_user(db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.delete_user(db, id)
