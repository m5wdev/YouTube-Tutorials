from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    blog_posts = relationship('Blog', back_populates='author')
