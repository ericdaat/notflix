from abc import ABC, abstractmethod

from application.templates.recommendations import Recommendations
from application.data_connector import Cache


class Engine(ABC):
    def __init__(self):
        self.cache = Cache()
        self.name = type(self).__name__

    @abstractmethod
    def recommend(self, context=None):
        r = Recommendations()
        r.engine_name = self.name
        r.ids = []
        r.scores = []

        return r

    @abstractmethod
    def update(self):
        return

    def recommendation_from_cache(self, key, recommendation):
        value = self.cache.get(key)

        if value:
            value = eval(value)
            assert isinstance(value, list)
            recommendation.ids = [v[0] for v in value]
            recommendation.scores = [v[1] for v in value]

        return recommendation
