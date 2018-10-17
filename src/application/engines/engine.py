from abc import ABC, abstractmethod

from application.reco.recommendations import Recommendations
from application.data_connector import Cache


class Engine(ABC):
    def __init__(self):
        self.cache = Cache()

    @abstractmethod
    def recommend(self):
        r = Recommendations()
        r.engine_name = type(self).__name__
        r.ids = []
        r.scores = []

        return r
