from abc import ABC, abstractmethod
import logging

from recommender.helpers import Recommendations
from config import MAX_RECOMMENDATIONS
from data.db import Engine as EngineTable
from data.db import get_session
from data.db import Recommendations as RecommendationsTable
from data.db import Product as ProductTable


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__
        logging.debug("Creating instance of {0}".format(self.type))

    @abstractmethod
    def recommend(self, active_product):
        r = Recommendations()
        r.type = self.type

        session = get_session()

        name, priority = session.query(EngineTable.display_name,
                                       EngineTable.priority)\
                                .filter(EngineTable.type == self.type)\
                                .one()

        r.display_name = name
        r.priority = priority

        return r


class QueryBasedEngine(Engine):
    def __init__(self):
        super(QueryBasedEngine, self).__init__()

    @abstractmethod
    def compute_query(self, session, active_product):
        pass

    def recommend(self, active_product):
        r = super(QueryBasedEngine, self).recommend(active_product)

        s = get_session()
        recommendations = self.compute_query(s, active_product)

        r.products = recommendations
        r.display_name = r.display_name.format(active_product.name)  # dynamic name

        logging.debug(r.to_string())

        return r.to_dict()


class OfflineEngine(QueryBasedEngine):
    def __init__(self):
        super(OfflineEngine, self).__init__()

    def compute_query(self, session, active_product):
        recommendations = session.query(ProductTable) \
            .filter(RecommendationsTable.source_product_id == active_product.id) \
            .filter(RecommendationsTable.engine_name == self.type) \
            .filter(ProductTable.id == RecommendationsTable.recommended_product_id) \
            .order_by(RecommendationsTable.score) \
            .limit(MAX_RECOMMENDATIONS).all()

        return recommendations

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def upload(self):
        pass


class OnlineEngine(Engine):
    def __init__(self):
        super(OnlineEngine, self).__init__()
        self.model = self.load_model()

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, active_product):
        pass

    @abstractmethod
    def train(self):
        pass

    def recommend(self, active_product):
        r = super(OnlineEngine, self).recommend(active_product)

        ids = self.predict(active_product)  # online prediction

        s = get_session()
        recommendations = s.query(ProductTable) \
            .filter(ProductTable.id.in_(ids)) \
            .filter(ProductTable.id != active_product.id) \
            .limit(MAX_RECOMMENDATIONS).all()

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()




