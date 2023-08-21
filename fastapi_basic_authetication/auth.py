from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db import get_db

from apps.user import db_queries


security = HTTPBasic()


def authenticate_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)):
    user = db_queries.get_user_by_username(db, username=str(credentials.username))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User {credentials.username} not found',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return user
