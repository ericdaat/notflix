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


def insert_in_db(to_insert):
    session = get_session()
    if isinstance(to_insert, list):
        session.bulk_save_objects(to_insert)
    else:
        session.add(to_insert)

    return session.commit()
