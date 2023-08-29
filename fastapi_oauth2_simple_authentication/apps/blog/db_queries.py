from sqlalchemy.orm.session import Session

from . import schemas, models


def get_all_blog_posts(db: Session):
    return db.query(models.Blog).all()


def get_blog(db: Session, id: int = None):
    return db.query(models.Blog).filter(models.Blog.id == id).first()


def create_blog(db: Session, request: schemas.BlogCreate):
    new_blog = models.Blog()
    new_blog.published = request.published
    new_blog.title = request.title
    new_blog.description = request.description
    new_blog.author_id = request.author_id

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
