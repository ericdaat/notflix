from .engine import QueryBasedEngine
from data.db import notflix
from config import MAX_RECOMMENDATIONS
from tracker.tracker import Tracker


class UserHistory(QueryBasedEngine):
    def __init__(self):
        super(UserHistory, self).__init__()

    def compute_query(self, session, context):
        tracker = Tracker()
        if context.user:
            views_history = tracker.get_views_history(key="history:{0}".format(context.user.username))

            recommendations = session.query(notflix.Product) \
                .filter(notflix.Product.id.in_(views_history)) \
                .limit(MAX_RECOMMENDATIONS) \
                .all()
        else:
            recommendations = []

        return recommendations
