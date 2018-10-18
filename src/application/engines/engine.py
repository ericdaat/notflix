from abc import ABC, abstractmethod

from application.templates.recommendations import Recommendations


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__

    @abstractmethod
    def recommend(self, context=None):
        r = Recommendations()
        r.type = self.type
        r.ids = []
        r.scores = []

        r.display_name = "Recommended for you"
        r.priority = 1

        return r

    @abstractmethod
    def update(self):
        return
