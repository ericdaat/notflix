from .engine import QueryBasedEngine
from src.data.model import movielens
from config import MAX_RECOMMENDATIONS


class UserHistory(QueryBasedEngine):
    def __init__(self):
        super(UserHistory, self).__init__()

    def compute_query(self, session, context):
        if context.user and context.history:
            recommendations = session.query(movielens.Movie) \
                .filter(movielens.Movie.id.in_(context.history)) \
                .limit(MAX_RECOMMENDATIONS) \
                .all()
        else:
            recommendations = []

        return recommendations
