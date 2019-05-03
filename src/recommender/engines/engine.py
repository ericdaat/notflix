from abc import ABC, abstractmethod
import logging
import os
import csv

from config import MAX_RECOMMENDATIONS, BATCH_UPLOAD_SIZE, ML_MODELS_PATH
from src.recommender.wrappers import Recommendations
from src.data_interface import model


class Engine(ABC):
    """ Abstract class for all engines.
    """
    def __init__(self):
        self.type = type(self).__name__
        self.input_id_kind = None
        logging.debug("Creating instance of {0}".format(self.type))

    @abstractmethod
    def recommend(self, context):
        """ Abstract method for all engines for recommending items.

        Args:
            context (recommender.wrappers.Context): the context

        Returns:
            recommender.wrappers.Recommendations: the recommendation object

        """
        r = Recommendations()
        r.type = self.type

        name, priority = model.Engine.query\
            .with_entities(model.Engine.display_name, model.Engine.priority)\
            .filter(model.Engine.type == self.type)\
            .one()

        if context.item and True:  # TODO: add dynamic name option in DB
            r.display_name = name.format(context.item.name)
        else:
            r.display_name = name

        r.priority = priority

        return r


class QueryBasedEngine(Engine):
    """ Abstract class for an engine based on a SQL query
    """
    def __init__(self):
        super(QueryBasedEngine, self).__init__()

    @abstractmethod
    def compute_query(self, context):
        """ Abstract method that computes the SQL query using SQLAlchemy

        Args:
            session: SQL Alchemy Session
            context (recommender.wrappers.Context): context

        Returns:
            query result

        """
        pass

    def recommend(self, context):
        """ Method for recommending items, by calling `self.compute_query`.

        Args:
            context (recommender.wrappers.Context): context

        Returns:
            list(dict): recommendations as list of dict

        """
        r = super(QueryBasedEngine, self).recommend(context)
        recommendations = self.compute_query(context)
        r.recommended_items = recommendations
        logging.debug(r.to_string())

        return r.to_dict()


class OfflineEngine(QueryBasedEngine):
    def __init__(self):
        super(OfflineEngine, self).__init__()
        self.output_filepath = os.path.join(
            ML_MODELS_PATH, "csv", self.type + ".csv"
        )

    def compute_query(self, context):
        recommendations = model.Movie.query\
            .filter(model.Movie.id == model.Recommendation.recommended_item_id) \
            .filter(model.Recommendation.source_item_id_kind == self.input_id_kind) \
            .filter(model.Recommendation.source_item_id == context.item.id) \
            .filter(model.Recommendation.engine_name == self.type) \
            .order_by(model.Recommendation.score.desc()) \
            .limit(MAX_RECOMMENDATIONS) \
            .all()

        return recommendations

    @abstractmethod
    def train(self):
        pass

    def save_recommendations_to_csv(self, recommendations):
        with open(self.output_filepath, "w") as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerows(recommendations)

    def upload(self):
        input_filepath = os.path.join(
            ML_MODELS_PATH,
            "csv",
            self.type + ".csv"
        )

        with open(input_filepath, "r") as csv_file:
            recommendations = []
            reader = csv.reader(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )

            for i, line in enumerate(reader):
                r = model.Recommendation(
                    engine_name=self.type,
                    source_item_id=line[0],
                    recommended_item_id=line[1],
                    source_item_id_kind=line[2],
                    score=line[3]
                )
                recommendations.append(r)

                # don't burst RAM, use batch size
                if i % BATCH_UPLOAD_SIZE == 0:
                    model.insert(recommendations)
                    logging.info("inserted {0} recommendations"
                                 .format(len(recommendations)))
                    del recommendations[:]
            else:
                model.insert(recommendations)
                logging.info("inserted {0} recommendations"
                             .format(len(recommendations)))
                del recommendations[:]


class OnlineEngine(Engine):
    def __init__(self):
        super(OnlineEngine, self).__init__()
        self.model = self.load_model()

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, context):
        pass

    @abstractmethod
    def train(self):
        pass

    def recommend(self, context):
        r = super(OnlineEngine, self).recommend(context)

        ids = self.predict(context)  # online prediction

        recommendations = model.Movie.query\
            .filter(model.Movie.id.in_(ids)) \
            .filter(model.Movie.id != context.item.id) \
            .limit(MAX_RECOMMENDATIONS).all()

        r.recommended_items = recommendations

        logging.debug(r.to_string())

        return r.to_dict()
