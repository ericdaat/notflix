import os
import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances

from src.data_interface import model
from src.recommender.engines import OfflineEngine
from src.utils.data import matrix_from_df_with_vect
from config import MAX_RECOMMENDATIONS, DATASETS_PATH, ML_MODELS_PATH


class ItemBasedCF(OfflineEngine):
    def __init__(self):
        super(ItemBasedCF, self).__init__()

    def compute_query(self, session, context):
        recommendations = session\
            .query(model.Movie) \
            .filter(model.Recommendation.source_item_id_kind == "item") \
            .filter(model.Recommendation.source_item_id == context.item.id) \
            .filter(model.Recommendation.engine_name == self.type) \
            .filter(model.Movie.id == model.Recommendation.recommended_item_id) \
            .order_by(model.Recommendation.score.desc()) \
            .limit(MAX_RECOMMENDATIONS) \
            .all()

        return recommendations

    def train(self):
        df = pd.read_csv(
            os.path.join(DATASETS_PATH, "movielens", "ml-1m", "ratings.csv")
        )

        v = CountVectorizer(token_pattern="[0-9]+")
        v.fit(df["movieId"].astype(str))

        X, movie_ids = matrix_from_df_with_vect(df, "movieId", "userId", v)

        cosine_sim = 1 - pairwise_distances(X, metric="cosine")

        recommendations = []

        for movie_index, movie_id in enumerate(movie_ids):
            sim_scores = list(enumerate(cosine_sim[movie_index]))
            sim_scores_sorted = sorted(
                sim_scores,
                key=lambda x: x[1], reverse=True
            )[:MAX_RECOMMENDATIONS]

            for recommended_movie_index, score in sim_scores_sorted:
                recommended_movie_id = movie_ids[recommended_movie_index]

                if movie_id == recommended_movie_id:
                    continue

                recommendations.append([
                    movie_id,
                    recommended_movie_id,
                    "item",
                    score
                ])

        # TODO: this should be an attribute for every offline engine
        output_filepath = os.path.join(
            ML_MODELS_PATH, "csv", self.type + ".csv"
        )

        # TODO: put this in another method, common to all offline engines
        with open(output_filepath, "w") as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerows(recommendations)
