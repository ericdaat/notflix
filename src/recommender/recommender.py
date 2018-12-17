import importlib
import sqlalchemy
import logging

import data.db
from utils.logging import setup_logging
from data.db import session, notflix


class Recommender(object):
    """ Recommender System base class.
    """
    def __init__(self):
        """ Recommender constructor.
        """
        setup_logging(log_dir="recommender",
                      config_path='recommender/logging.yml')

        self.engines = []

        for engine_type in session.query(notflix.Engine.type).all():
            module = importlib.import_module("recommender.engines")
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines.append(instance)

    def recommend(self, context):
        """ Make recommendations

        Args:
            context (recommender.wrappers.Context): the context

        Returns:
            list(dict): List of recommendations as dictionaries
        """
        recommendation_list = []

        active_engines = []
        if context.page_type:
            try:
                active_engines = session.query(data.db.Page.engines) \
                                        .filter(data.db.Page.name == context.page_type) \
                                        .one()[0]
            except sqlalchemy.orm.exc.NoResultFound:
                pass

        logging.debug("active engines: {0}".format(active_engines))

        for e in self.engines:
            if e.type not in active_engines:
                continue

            recommendations = e.recommend(context)
            if len(recommendations["products"]) > 0:
                recommendation_list.append(recommendations)

        return recommendation_list
