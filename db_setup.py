import sys

from sqlalchemy import Column, ForeignKey, Integer, String

# will use when create mapper
from sqlalchemy.ext.declarative import declarative_base

# will use when create mapper
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()
    
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class Item(Base):
    __tablename__ = 'item'
    cat_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String(1000), nullable = False)
    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    category = relationship(Category)
    
    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
