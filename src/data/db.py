from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import DB_HOST

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Engine(Base):
    __tablename__ = "engine"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    type = Column(String(20), nullable=False)
    display_name = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    name = Column(String(256), nullable=False)
    price = Column(Float, nullable=True)
    genres = Column(String(256), nullable=True)
    image = Column(String(256), nullable=True)
    description = Column(String(512), nullable=True)
    year = Column(Date, nullable=True)
    rating = Column(Float, nullable=True)
    director = Column(String(256), nullable=True)
    actors = Column(String(256), nullable=True)
    awards = Column(String(256), nullable=True)
    language = Column(String(256), nullable=True)
    country = Column(String(256), nullable=True)
    duration = Column(Integer, nullable=True)


def setup():
    engine = create_engine(DB_HOST)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session():
    engine = create_engine(DB_HOST)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


def insert(to_insert):
    session = get_session()
    if isinstance(to_insert, list):
        session.bulk_save_objects(to_insert)
    else:
        session.add(to_insert)

    return session.commit()