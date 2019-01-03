from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Binary
from sqlalchemy.dialects import postgresql
from data.db import Base


class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    engine_name = Column(String(56), nullable=False)
    source_product_id = Column(Integer, nullable=False)
    recommended_product_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String(56), nullable=False, unique=True)
    engines = Column(postgresql.ARRAY(String(56)))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email = Column(String(255), unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(Binary(60), nullable=False)

    favorite_genres = Column(postgresql.ARRAY(Integer))
