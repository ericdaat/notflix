import importlib
import sqlalchemy
import logging

from src.data.model import db_scoped_session, common


class Recommender(object):
    """ Recommender System base class.
    """
    def __init__(self):
        """ Recommender constructor.
        """

        self.engines = {}

        for engine_type in db_scoped_session.query(common.Engine.type).all():
            module = importlib.import_module("src.recommender.engines")
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines[instance.type] = instance

    def recommend(self, context, restrict_to_engines=[]):
        """ Make recommendations

        Args:
            context (recommender.wrappers.Context): the context

        Returns:
            list(dict): List of recommendations as dictionaries
        """
        recommendation_list = []

        active_engines = restrict_to_engines

        if not active_engines and context.page_type:
            try:
                active_engines = db_scoped_session\
                    .query(common.Page.engines)\
                    .filter(common.Page.name == context.page_type)\
                    .one()[0]
            except sqlalchemy.orm.exc.NoResultFound:
                pass

        logging.debug("active engines: {0}".format(active_engines))

        for type, instance in self.engines.items():
            if type not in active_engines:
                continue

            recommendations = instance.recommend(context)

            if len(recommendations["recommended_items"]) > 0:
                recommendation_list.append(recommendations)

        return recommendation_list
