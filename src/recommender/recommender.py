import importlib
import sqlalchemy
import logging

from src.data_interface import model


class Recommender(object):
    """ Recommender System base class.
    """
    def __init__(self):
        """ Recommender constructor.
        """
        # Engines are created once at runtime
        self.engines = {}

        # Query the registered engines in DB and create their instances
        engine_types = \
            model.Engine.query.with_entities(model.Engine.type).all()

        for engine_type in engine_types:
            module = importlib.import_module("src.recommender.engines")
            # TODO: handle a non existing engine
            class_ = getattr(module, engine_type[0])
            instance = class_()
            self.engines[instance.type] = instance

    def recommend(self, context, restrict_to_engines=[]):
        """ Call all the active engines based on a context\
            and return their recommendations.

        It is possible to restrict to a list of engines by using the\
        ``restrict_to_engines`` parameter.

        Args:
            context (recommender.wrappers.Context): Context wrapper,\
                providing informations about the current item or user\
                or session.

        Returns:
            list(dict): List of recommendations as dictionaries
        """
        recommendation_list = []

        active_engines = []

        # If no engine restriction and page_type in context,
        # get active engines in DB
        if not restrict_to_engines and context.page_type:
            try:
                active_engines = model.Page.query\
                    .with_entities(model.Page.engines)\
                    .filter(model.Page.name == context.page_type)\
                    .one()[0]
            except sqlalchemy.orm.exc.NoResultFound:
                pass
        elif restrict_to_engines:
            active_engines = restrict_to_engines

        logging.debug("active engines: {0}".format(active_engines))

        for engine_type, instance in self.engines.items():
            if engine_type not in active_engines:
                continue

            # recommendations for each engine
            recommendations = instance.recommend(context)

            if len(recommendations["recommended_items"]) > 0:
                recommendation_list.append(recommendations)

        # sort recomemndations based on engines priority
        recommendation_list = sorted(
            recommendation_list,
            key=lambda r: r["priority"]
        )

        return recommendation_list
