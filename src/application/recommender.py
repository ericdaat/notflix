from application.engines import CacheBasedEngine
from application.utils.logging import setup_logging


class Recommender(object):
    def __init__(self):
        setup_logging(default_path='application/logging.yml')
        self.engines = [CacheBasedEngine()]

    def recommend(self, context=None):
        for e in self.engines:
            print(e.recommend(context))
