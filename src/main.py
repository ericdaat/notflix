from sqlalchemy import create_engine
from application.recommender import Recommender
from application.templates.context import Context
from data_connector.utils import insert_in_db, DB_HOST
from data_connector.models import Engine as EngineTable


if __name__ == "__main__":
    engine = create_engine(DB_HOST)
    EngineTable.__table__.drop(bind=engine)
    EngineTable.__table__.create(bind=engine)

    insert_in_db(EngineTable(**{"type": "DBBasedEngine",
                                "display_name": "Similar to {0}",
                                "priority": 0}))

    # insert_in_db(EngineTable(**{"type": "MLBasedEngine",
    #                             "display_name": "Machine Learning says this",
    #                             "priority": 1}))

    r = Recommender()
    c = Context(item_id=100, user_id=3)
    print(r.recommend(c))
