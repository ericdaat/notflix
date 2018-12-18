from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from data.db import Base


def init(db_host):
    engine = create_engine(db_host)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session(db_host):
    engine = create_engine(db_host)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


def insert(to_insert, db_host):
    session = get_session(db_host)
    if isinstance(to_insert, list):
        session.bulk_save_objects(to_insert)
    else:
        session.add(to_insert)

    return session.commit()