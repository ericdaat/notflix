from abc import ABC, abstractmethod
import logging
from recommender.helpers import Recommendations
from config import MAX_RECOMMENDATIONS
from data.db import session, notflix


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__
        logging.debug("Creating instance of {0}".format(self.type))

    @abstractmethod
    def recommend(self, active_product):
        r = Recommendations()
        r.type = self.type

        name, priority = session.query(notflix.Engine.display_name,
                                       notflix.Engine.priority)\
                                .filter(notflix.Engine.type == self.type)\
                                .one()

        if active_product and True:  # TODO: add dynamic name option in DB
            r.display_name = name.format(active_product.name)
        else:
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

        recommendations = self.compute_query(session, active_product)

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()


class OfflineEngine(QueryBasedEngine):
    def __init__(self):
        super(OfflineEngine, self).__init__()

    def compute_query(self, session, active_product):
        recommendations = session.query(notflix.Product) \
            .filter(notflix.Recommendations.source_product_id == active_product.id) \
            .filter(notflix.Recommendations.engine_name == self.type) \
            .filter(notflix.Product.id == notflix.Recommendations.recommended_product_id) \
            .order_by(notflix.Recommendations.score) \
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

        recommendations = session.query(notflix.Product) \
            .filter(notflix.Product.id.in_(ids)) \
            .filter(notflix.Product.id != active_product.id) \
            .limit(MAX_RECOMMENDATIONS).all()

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()




