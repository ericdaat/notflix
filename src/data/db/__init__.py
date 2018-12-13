import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

DB_HOST = "postgresql://{user}:{password}@{host}/{db}".format(
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    db=os.environ.get("POSTGRES_DB"),
    host=os.environ.get("HOST")
)

engine = create_engine(DB_HOST, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()
Base.query = session.query_property()


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


