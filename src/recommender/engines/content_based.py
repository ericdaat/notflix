from recommender.engines.engine import QueryBasedEngine, OfflineEngine
from data.db import Product as ProductTable


class SameGenres(QueryBasedEngine):
    def __init__(self):
        super(SameGenres, self).__init__()

    def compute_query(self, session, active_product):
        recommendations = session.query(ProductTable)\
                           .filter(ProductTable.genres == active_product.genres)\
                           .filter(ProductTable.id != active_product.id)\
                           .limit(10).all()

        return recommendations


class TfidfGenres(OfflineEngine):
    def __init__(self):
        super(TfidfGenres, self).__init__()