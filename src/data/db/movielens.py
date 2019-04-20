
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.dialects import postgresql
from src.data.db import Base, BaseTable


class Movie(Base, BaseTable):
    __tablename__ = "movies"
    name = Column(String(256), nullable=False)
    genres = Column(postgresql.ARRAY(Integer), nullable=True)
    image = Column(String(256), nullable=True)
    description = Column(String(512), nullable=True)
    year = Column(Date, nullable=True)
    rating = Column(Float, nullable=True)
    director = Column(String(1024), nullable=True)
    actors = Column(String(256), nullable=True)
    awards = Column(String(256), nullable=True)
    language = Column(String(256), nullable=True)
    country = Column(String(256), nullable=True)
    duration = Column(Integer, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Genre(Base, BaseTable):
    __tablename__ = "genres"
    name = Column(String(56), nullable=False, unique=True)
