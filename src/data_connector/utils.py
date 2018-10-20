from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from data_connector.models import Base
from config import DB_HOST


def setup_db():
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


def insert_in_db(item):
    session = get_session()
    session.add(item)
    session.commit()

    return 0
