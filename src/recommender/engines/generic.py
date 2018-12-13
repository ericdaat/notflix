from .engine import QueryBasedEngine
from data.db import notflix
from config import MAX_RECOMMENDATIONS


class TopRated(QueryBasedEngine):
    def __init__(self):
        super(TopRated, self).__init__()

    def compute_query(self, session, active_product):
        recommendations = session.query(notflix.Product) \
            .order_by(notflix.Product.rating.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS).all()

        return recommendations


class MostRecent(QueryBasedEngine):
    def __init__(self):
        super(MostRecent, self).__init__()

    def compute_query(self, session, active_product):
        recommendations = session.query(notflix.Product) \
            .order_by(notflix.Product.year.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS).all()

        return recommendations

