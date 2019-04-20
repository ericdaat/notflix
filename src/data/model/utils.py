from sqlalchemy_utils import database_exists, create_database
from src.data.model import Base, engine, db_session


def init():
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert(to_insert):
    session = db_session()

    if isinstance(to_insert, list):
        session.bulk_save_objects(to_insert)
    else:
        session.add(to_insert)

    return session.commit()
