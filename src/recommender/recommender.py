import importlib
from utils.logging import setup_logging
from data.db import session
from data.db import Engine as EngineTable
from data.db import Product as ProductTable


class Recommender(object):
    """ Recommender System base class.
    """
    def __init__(self):
        """ Recommender constructor.
        Instantiates all the active engines.
        """
        setup_logging(log_dir="recommender",
                      config_path='recommender/logging.yml')

        self.engines = []

        for engine_type in session.query(EngineTable.type).all():
            module = importlib.import_module("recommender.engines")
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines.append(instance)

    def recommend(self, context=None, specific_engines=None):
        """ Make recommendations
        :param templates.Context context:
        :param list<str> specific_engines:
        :return: List of recommendations
        :rtype: list(dict)
        """
        recommendation_list = []

        if context.item_id:
            active_product = session.query(ProductTable)\
                                    .filter(ProductTable.id == context.item_id)\
                                    .one()
        else:
            active_product = None

        for e in self.engines:
            if specific_engines and e.type not in specific_engines:
                continue

            recommendations = e.recommend(active_product)
            if len(recommendations["products"]) > 0:
                recommendation_list.append(recommendations)

        return recommendation_list
