from application.recommender import Recommender
from application.templates.context import Context
from data_connector.utils import setup_db, insert_in_db
from data_connector.db import Engine, Product


if __name__ == "__main__":
    setup_db()

    insert_in_db(Engine(**{"type": "CacheBasedEngine",
                           "display_name": "You might also like",
                           "priority": 0}))

    insert_in_db(Product(**{"name": "Titanic",
                            "price": 3.3}))

    r = Recommender()
    c = Context(item_id=100, user_id=3)
    r.recommend(c)
