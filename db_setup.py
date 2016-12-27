# database setup file for creating database of the Application
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# A Table Containing Data Of all the Users
class User(Base):
    __tablename__ = 'user'

    name = Column(String(50),  nullable=False)
    email = Column(String(50), nullable=False)
    picture = Column(String(150))
    id = Column(Integer, primary_key=True)


# A Table Containing Data Of all the TV Serieses
class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    actors = Column(String(250), nullable=False)
    rating = Column(Float(precision=1))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Function that return serieses data in easily serializeable format
    @property
    def serialize(self):
    	return {
            'name': self.name,
            'id': self.id,
            'actors': self.actors,
            'rating': self.rating,
            }


# A Table Containing Data Of all episodes in an TV Series
class Episode(Base):
    __tablename__ = 'episode'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    air_date = Column(String(20))
    description = Column(String(250), nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'))
    series = relationship(Series)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Function that return data of every episode in easily serializeable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'air_date': self.air_date,
            }

engine = create_engine('sqlite:///series.db')

Base.metadata.create_all(engine)
