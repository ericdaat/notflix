from application.recommender import Recommender
from application.templates.context import Context


if __name__ == "__main__":
    r = Recommender()
    c = Context(item_id=100, user_id=3)
    r.recommend(c)
