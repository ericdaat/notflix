from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_connector.db import Base
from config import DB_HOST


def setup_db():
    engine = create_engine(DB_HOST)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_in_db(item):
    engine = create_engine(DB_HOST)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.add(item)
    session.commit()

    return 0
