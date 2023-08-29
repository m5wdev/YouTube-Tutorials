from sqlalchemy.orm.session import Session

from . import schemas, models
from apps.auth.hash_password import HashPassword


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, id: int = None, email: str = None, username: str = None):
    if id:
        return db.query(models.User).filter(models.User.id == id).first()
    if email:
        return db.query(models.User).filter(models.User.email == email).first()
    if username:
        return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, request: schemas.UserCreate):
    new_user = models.User()
    new_user.username = request.username
    new_user.email = request.email
    new_user.password = HashPassword.bcrypt(request.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # get id to new user
    return new_user


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    db_user = get_user(db, id=user_id)
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = HashPassword.bcrypt(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, id: int):
    db_user = get_user(db, id=id)
    db.delete(db_user)
    db.commit()
    return db_user
