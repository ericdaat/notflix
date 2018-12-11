from sqlalchemy import create_engine
from data.db import insert, DB_HOST
from data.db import Engine as EngineTable
from recommender.engines.content_based import TfidfGenres, TopRated


def register():
    engine = create_engine(DB_HOST)
    EngineTable.__table__.drop(bind=engine, checkfirst=True)
    EngineTable.__table__.create(bind=engine, checkfirst=True)

    insert(EngineTable(**{"type": "SameGenres",
                          "display_name": "Similar to {0}",
                          "priority": 1}))


def train():
    trainable_engines = [TfidfGenres()]

    for engine in trainable_engines:
        engine.train()
        engine.upload()


if __name__ == "__main__":
    register()
    # train()
