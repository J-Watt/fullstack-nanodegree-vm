# ------------------------------------------------------------------------------
# Name:         database_setup
# Purpose:      SQLAlchemy ORM for catalog application database
#
# Author:       Jordan Alexander Watt
#
# Modified:     5-2-2016
# Created:      12-1-2015
# ------------------------------------------------------------------------------

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Item(Base):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    image = Column(String(250))
    description = Column(String(250))
    date = Column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'description': self.description
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
