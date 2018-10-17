from application.engines import FirstEngine
from application.utils.logging import setup_logging
from application.templates.context import Context


class Recommender(object):
    def __init__(self):
        setup_logging(default_path='application/logging.yml')
        self.engines = [FirstEngine()]

    def recommend(self):
        c = Context()
        c.item_id = 100

        for e in self.engines:
            print(e.recommend(c))
