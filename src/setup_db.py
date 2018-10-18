from application.data_connector.db import Base, Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    engine = create_engine("mysql://root@localhost/recommender")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_engine = Engine(type="CacheBasedEngine",
                        display_name="You might like",
                        priority=0)
    session.add(new_engine)
    session.commit()
