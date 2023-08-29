from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWTError

from sqlalchemy.orm import Session
from db import get_db
from apps.user.db_queries import get_user


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = '52367badbf4e42f3a94d9ce456e1f01cbfee36a604da5c9589fa84f0bb9e661b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authneticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        decode_username: str = payload.get('username')

        if decode_username is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption

    # TODO: check if token expires

    user = get_user(db, username=decode_username)

    if user is None:
        raise credentials_exeption

    return user
