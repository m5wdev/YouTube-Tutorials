from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


# class Category(Base):
#     __tablename__ = 'category'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    published = Column(Boolean, default=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='blog_posts')
    # category = relationship('Category', back_populates='category')
