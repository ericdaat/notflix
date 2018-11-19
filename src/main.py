from sqlalchemy import create_engine
from application.recommender import Recommender
from application.helpers import Context
from data.db import insert, DB_HOST
from data.db import Engine as EngineTable


if __name__ == "__main__":
    engine = create_engine(DB_HOST)
    EngineTable.__table__.drop(bind=engine)
    EngineTable.__table__.create(bind=engine)

    insert(EngineTable(**{"type": "DBBasedEngine",
                          "display_name": "Similar to {0}",
                          "priority": 0}))

    insert(EngineTable(**{"type": "MLBasedEngine",
                          "display_name": "You might also like",
                          "priority": 1}))

    r = Recommender()
    c = Context(item_id=1502, user_id=3)
    print(r.recommend(c))
