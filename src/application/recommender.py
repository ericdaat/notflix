import importlib
from application.utils.logging import setup_logging
from data_connector.utils import get_session
from data_connector.models import Engine as EngineTable


class Recommender(object):
    def __init__(self):
        setup_logging(default_path='application/logging.yml')

        self.engines = []

        session = get_session()
        for engine_type in session.query(EngineTable.type).all():
            module = importlib.import_module("application.engines")
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines.append(instance)

    def recommend(self, context=None):
        for e in self.engines:
            print(e.recommend(context))
