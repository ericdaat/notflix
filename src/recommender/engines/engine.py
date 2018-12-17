from abc import ABC, abstractmethod
import logging

from recommender.wrappers import Recommendations
from config import MAX_RECOMMENDATIONS
from data import db
from data.db import session, notflix


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__
        logging.debug("Creating instance of {0}".format(self.type))

    @abstractmethod
    def recommend(self, context):
        r = Recommendations()
        r.type = self.type

        name, priority = session.query(notflix.Engine.display_name,
                                       notflix.Engine.priority)\
                                .filter(notflix.Engine.type == self.type)\
                                .one()

        if context.item and True:  # TODO: add dynamic name option in DB
            r.display_name = name.format(context.item.name)
        else:
            r.display_name = name

        r.priority = priority

        return r


class QueryBasedEngine(Engine):
    def __init__(self):
        super(QueryBasedEngine, self).__init__()

    @abstractmethod
    def compute_query(self, session, context):
        pass

    def recommend(self, context):
        r = super(QueryBasedEngine, self).recommend(context)

        recommendations = self.compute_query(session, context)

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()


class OfflineEngine(QueryBasedEngine):
    def __init__(self):
        super(OfflineEngine, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Product) \
            .filter(db.Recommendation.source_product_id == context.item.id) \
            .filter(db.Recommendation.engine_name == self.type) \
            .filter(notflix.Product.id == db.Recommendation.recommended_product_id) \
            .order_by(db.Recommendation.score) \
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
    def predict(self, context):
        pass

    @abstractmethod
    def train(self):
        pass

    def recommend(self, context):
        r = super(OnlineEngine, self).recommend(context)

        ids = self.predict(context)  # online prediction

        recommendations = session.query(notflix.Product) \
            .filter(notflix.Product.id.in_(ids)) \
            .filter(notflix.Product.id != context.item.id) \
            .limit(MAX_RECOMMENDATIONS).all()

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()




