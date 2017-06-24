import sys

from sqlalchemy import Column, ForeignKey, Integer, String

# will use when create mapper
from sqlalchemy.ext.declarative import declarative_base

# will use when create mapper
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'item'
    cat_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String(1000), nullable=False)
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
