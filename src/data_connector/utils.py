from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_connector.db import Base, Engine
from config import DB_HOST


def setup_db():
    engine = create_engine(DB_HOST)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def new_recommender_engine(kwargs):
    engine = create_engine(DB_HOST)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_engine = Engine(**kwargs)
    session.add(new_engine)
    session.commit()

    return 0
