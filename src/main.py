from application.recommender import Recommender
from application.templates.context import Context
from data_connector.utils import setup_db, new_recommender_engine


if __name__ == "__main__":
    setup_db()
    new_recommender_engine({"type": "CacheBasedEngine",
                            "display_name": "You might also like",
                            "priority": 0})

    r = Recommender()
    c = Context(item_id=100, user_id=3)
    r.recommend(c)
