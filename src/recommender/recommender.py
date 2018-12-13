import importlib
from utils.logging import setup_logging
from data.db import session, notflix


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

        for engine_type in session.query(notflix.Engine.type).all():
            module = importlib.import_module("recommender.engines")
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines.append(instance)

    def recommend(self, context=None):
        """ Make recommendations
        :param templates.Context context:
        :return: List of recommendations
        :rtype: list(dict)
        """
        recommendation_list = []
        active_product = None

        if context.item_id:
            active_product = session.query(notflix.Product)\
                                    .filter(notflix.Product.id == context.item_id)\
                                    .one()

        active_engines = []
        if context.page_type:
            active_engines = session.query(notflix.Page.engines) \
                                    .filter(notflix.Page.name == context.page_type) \
                                    .one()[0]

        for e in self.engines:
            if e.type not in active_engines:
                continue

            recommendations = e.recommend(active_product)
            if len(recommendations["products"]) > 0:
                recommendation_list.append(recommendations)

        return recommendation_list
