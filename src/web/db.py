from config import DB_HOST
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from data_connector.models import Base


engine = create_engine(DB_HOST, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(engine)



