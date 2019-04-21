from .engine import QueryBasedEngine
from src.data_interface import model
from config import MAX_RECOMMENDATIONS


class UserHistory(QueryBasedEngine):
    def __init__(self):
        super(UserHistory, self).__init__()

    def compute_query(self, session, context):
        if context.user and context.history:
            recommendations = session.query(model.Movie) \
                .filter(model.Movie.id.in_(context.history)) \
                .limit(MAX_RECOMMENDATIONS) \
                .all()
        else:
            recommendations = []

        return recommendations
