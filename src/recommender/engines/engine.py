from abc import ABC, abstractmethod
import logging
import os
import csv

from config import MAX_RECOMMENDATIONS, BATCH_UPLOAD_SIZE, ML_MODELS_PATH
from src.recommender.wrappers import Recommendations
from src.data_interface import model
from sqlalchemy.sql.expression import case


class Engine(ABC):
    """ Abstract class for all engines. You should not directly use this
    class, instead use the classes that inherit from this class.
    """
    def __init__(self):
        self.type = type(self).__name__  # the engine type is its class name

        # ``input_id_kind`` tells what id the engine is expecting.
        # It can be "item" if the engine is expecting an item_id,
        # or "user" if it expects a user_id
        self.input_id_kind = None

        logging.debug("Creating instance of {0}".format(self.type))

    def init_recommendations(self, context):
        """ Create an empty ``src.recommender.wrappers.Recommendations```
        object and fill in the engine type, display name and priority
        based on the informations stored in DB.

        Args:
            context (src.recommender.wrappers.Context): Context wrapper,
                containing useful informations for the engine.

        Returns:
            (src.recommender.wrappers.Recommendations): Recommendations object\
                filled with engine type, display name and priority
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

    @abstractmethod
    def recommend(self, context):
        """ Abstract method for all engines for recommending items.

        The context wrapper stores all the informations the engine might
        need to compute the recommendations, like the current item_id,
        the current user_id, the user browsing history, etc ...

        Every engine must override this method. They have to call
        ``self.init_recommendations`` first to create an empty
        ``src.recommender.wrappers.Recommendations`` object and then
        enrich it with the recommended items.

        Args:
            context (src.recommender.wrappers.Context): the context

        Returns:
            src.recommender.wrappers.Recommendations: the recommendation object
        """


class QueryBasedEngine(Engine):
    """ Abstract class for an engine based on a SQL query
    performed at every call. These are engines require no training,
    for instance an engine that will recommend random items for DB.
    """
    def __init__(self):
        super(QueryBasedEngine, self).__init__()

    @abstractmethod
    def compute_query(self, context):
        """ Abstract method that computes the SQL query using SQLAlchemy

        Args:
            context (recommender.wrappers.Context): context wrapper

        Returns:
            query result

        """
        pass

    def recommend(self, context):
        """ Method for recommending items, by calling `self.compute_query`.

        Args:
            context (recommender.wrappers.Context): context wrapper

        Returns:
            list(dict): recommendations as list of dict

        """
        r = self.init_recommend(context)
        recommendations = self.compute_query(context)
        r.recommended_items = recommendations
        logging.debug(r.to_string())

        return r.to_dict()


class OfflineEngine(QueryBasedEngine):
    """ These engines are a special kind of QueryBasedEngine because they
    require a training.

    Most of the offline Machine Learning algorithms will inherit from
    this class.

    The recommendations are computed offline with the ``train`` method,
    then saved on disk with ``save_recommendations_to_csv``
    and finally uploaded to the DB using ``upload``.
    """
    def __init__(self):
        super(OfflineEngine, self).__init__()
        self.output_filepath = os.path.join(
            ML_MODELS_PATH, "csv", self.type + ".csv"
        )

    def compute_query(self, context):
        """Get the recommended items from the DB.

        Args:
            context (src.recommender.wrappers.Context): Context wrapper

        Returns:
            list: list of Recommendation
        """
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
        """ Method for training the engine.
        This method should load the dataset, compute the recommendations
        and then persist them to disk using ``save_recommendations_to_csv``.
        """
        pass

    def save_recommendations_to_csv(self, recommendations):
        """ Save recommendations to a CSV file.

        Args:
            recommendations (list(tuple)): List of recommendation tuple\
            corresponding to:\
            (movie_id, recommended_movie_id, input_kind, score)
        """
        with open(self.output_filepath, "w") as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerows(recommendations)

    def upload(self):
        """ Upload the recommendations from a CSV file to the DB.
        """
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
            else:  # last batch
                model.insert(recommendations)
                logging.info("inserted {0} recommendations"
                             .format(len(recommendations)))
                del recommendations[:]


class OnlineEngine(Engine):
    """ Online Machine Learning Engines that do not get their recommendations
    from a SQL query but from a loaded model.

    The model is trained with the ``train`` method, and loaded at runtime
    with the ``load_model`` method.
    """
    def __init__(self):
        super(OnlineEngine, self).__init__()
        self.model = self.load_model()

    @abstractmethod
    def load_model(self):
        """ Load the ML model from disk and return it

        Returns:
            The ML model to be saved as ``self.model``
        """
        model = None

        return model

    @abstractmethod
    def predict(self, context):
        """ Predict using the loaded model and the context.

        Args:
            context (src.recommender.wrappers.Context): Context wrapper

        Returns:
            ids (list(int)): list of recommended ids\
                sorted by descending score
            scores (list(float)): list of scores for each recommended item
        """

        ids, scores = None, None

        return ids, scores

    @abstractmethod
    def train(self):
        """ Train a ML model and save it to disk
        """
        pass

    def recommend(self, context):
        """ Recommend movies based on context

        Args:
            context (src.recommender.wrappers.Context): Context wrapper

        Returns:
            recommendations (dict): src.recommender.wrappers.Recommendations\
                as dict
        """
        r = self.init_recommendations(context)

        ids, _ = self.predict(context)  # online prediction

        if ids:
            # considering the ids are ranked from the most relevant to
            # the least relevant, use this to keep the order of
            # the recommendations when querying the DB.
            ordering = case(
                {id: index for index, id in enumerate(ids)},
                value=model.Movie.id
            )

            recommendations = model.Movie.query\
                .filter(model.Movie.id.in_(ids)) \
                .order_by(ordering) \
                .limit(MAX_RECOMMENDATIONS).all()
        else:
            recommendations = []

        r.recommended_items = recommendations

        logging.debug(r.to_string())

        return r.to_dict()
