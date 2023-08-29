from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from sqlalchemy.orm import Session
from db import get_db

from apps.auth.oauth2 import oauth2_schema, get_current_user

from . import schemas, db_queries


router = APIRouter(
    prefix='/blog',
    tags=['blog'],
)


@router.get('/get-all', response_model=List[schemas.BlogDetail])
# async def get_all(db: Session = Depends(get_db)):
async def get_all(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    return db_queries.get_all_blog_posts(db)


@router.get('/{id}')
# @router.get('/{id}', response_model=schemas.BlogDetail)
# async def get_blog(id: int = None, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
async def get_blog(id: int = None, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    blog = db_queries.get_blog(db, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no blog post in db')
    # return blog
    return {
        'data': blog,
        'current_user': current_user
    }


@router.post('/create', response_model=schemas.BlogCreate)
async def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)):
    return db_queries.create_blog(db, request)
