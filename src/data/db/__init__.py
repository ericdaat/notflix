from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DB_HOST

engine = create_engine(DB_HOST, convert_unicode=True)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_scoped_session = scoped_session(db_session)

Base = declarative_base()
Base.query = db_scoped_session.query_property()