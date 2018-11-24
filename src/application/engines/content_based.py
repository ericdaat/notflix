import logging

from application.engines.engine import Engine
from data.db import get_session
from data.db import Product as ProductTable
from data.db import Recommendations as RecommendationsTable


class SameGenres(Engine):
    def __init__(self):
        super(SameGenres, self).__init__()

    def recommend(self, active_product):
        r = super(SameGenres, self).recommend(active_product)

        s = get_session()
        recommendations = s.query(ProductTable)\
                           .filter(ProductTable.genres == active_product.genres)\
                           .filter(ProductTable.id != active_product.id)\
                           .limit(10).all()

        r.products = recommendations
        r.display_name = r.display_name.format(active_product.name)  # dynamic name

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        pass


class TfidfGenres(Engine):
    def __init__(self):
        super(TfidfGenres, self).__init__()

    def recommend(self, active_product):
        r = super(TfidfGenres, self).recommend(active_product)

        s = get_session()
        recommendations = s.query(ProductTable) \
            .filter(RecommendationsTable.source_product_id == active_product.id) \
            .filter(RecommendationsTable.engine_name == self.type) \
            .filter(ProductTable.id == RecommendationsTable.recommended_product_id) \
            .order_by(RecommendationsTable.score) \
            .limit(10).all()

        r.products = recommendations
        r.display_name = r.display_name.format(active_product.name)  # dynamic name

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        pass
