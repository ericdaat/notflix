import os
import logging
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Binary, Date, DateTime
)
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DB_HOST


engine = create_engine(DB_HOST, convert_unicode=True)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_scoped_session = scoped_session(db_session)

Base = declarative_base()
Base.query = db_scoped_session.query_property()


class BaseTable(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


def init():
    if not database_exists(engine.url):
        create_database(engine.url)
        logging.info("Created database {0}".format(os.environ["POSTGRES_DB"]))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert(to_insert):
    session = db_session()

    if isinstance(to_insert, list):
        session.bulk_save_objects(to_insert)
    else:
        session.add(to_insert)

    return session.commit()


class Recommendation(Base, BaseTable):
    __tablename__ = "recommendations"
    engine_name = Column(String(56), nullable=False)
    source_item_id = Column(Integer, nullable=False)
    recommended_item_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)


class Page(Base, BaseTable):
    __tablename__ = "pages"
    name = Column(String(56), nullable=False, unique=True)
    engines = Column(postgresql.ARRAY(String(56)))


class Engine(Base, BaseTable):
    __tablename__ = "engines"
    type = Column(String(20), nullable=False)
    display_name = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)


class User(Base, BaseTable):
    __tablename__ = "users"
    email = Column(String(255), unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(Binary(60), nullable=False)
    favorite_genres = Column(postgresql.ARRAY(Integer))


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
