from config import DB_HOST
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from data.db import Base


engine = create_engine(DB_HOST, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

