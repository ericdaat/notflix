from sqlalchemy import Column, Integer, String, Float, Binary
from sqlalchemy.dialects import postgresql
from src.data.db import Base, BaseTable


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
