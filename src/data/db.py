from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from config import DB_HOST

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(DB_HOST, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))


class Engine(Base):
    __tablename__ = "engines"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    type = Column(String(20), nullable=False)
    display_name = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    name = Column(String(256), nullable=False)
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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Recommendations(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    engine_name = Column(String(56), nullable=False)
    source_product_id = Column(Integer, nullable=False)
    recommended_product_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    name = Column(String(56), nullable=False, unique=True)


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    name = Column(String(56), nullable=False, unique=True)
    engines = Column(ARRAY(String(56)))


def init():
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
