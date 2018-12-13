from sqlalchemy import create_engine
from data.db import insert, DB_HOST, notflix
from recommender.engines.content_based import TfidfGenres


def register():
    engine = create_engine(DB_HOST)
    notflix.Engine.__table__.drop(bind=engine, checkfirst=True)
    notflix.Engine.__table__.create(bind=engine, checkfirst=True)

    insert(notflix.Engine(**{"type": "SameGenres",
                             "display_name": "Similar to {0}",
                             "priority": 1}))

    insert(notflix.Engine(**{"type": "TopRated",
                             "display_name": "Top rated movies",
                             "priority": 1}))

    insert(notflix.Engine(**{"type": "MostRecent",
                             "display_name": "Recent movies",
                             "priority": 1}))


def train():
    trainable_engines = [TfidfGenres()]

    for engine in trainable_engines:
        engine.train()
        engine.upload()


if __name__ == "__main__":
    register()
    # train()
