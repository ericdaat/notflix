from application.engines import FirstEngine
from application.utils.logging import setup_logging


class Recommender(object):
    def __init__(self):
        setup_logging(default_path='application/logging.yml')
        self.engines = [FirstEngine()]

    def recommend(self):
        return self.engines[0].recommend()
