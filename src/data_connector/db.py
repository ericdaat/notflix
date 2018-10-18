import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Engine(Base):
    __tablename__ = "engine"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)
    type = Column(String(20), nullable=False)
    display_name = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)
