import csv
import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from recommender.engines.engine import QueryBasedEngine, OfflineEngine
from config import MAX_RECOMMENDATIONS
from data.db import notflix, common, utils, DB_HOST


class SameGenres(QueryBasedEngine):
    def __init__(self):
        super(SameGenres, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Product)\
                           .filter(notflix.Product.genres.contains([g[0] for g in context.item.genres]))\
                           .filter(notflix.Product.id != context.item.id) \
                           .limit(MAX_RECOMMENDATIONS).all()

        return recommendations


class TfidfGenres(OfflineEngine):
    def __init__(self):
        super(TfidfGenres, self).__init__()

    def train(self):
        movies = pd.read_csv("data/datasets/movielens/ml-20m/movies.csv")

        vec = TfidfVectorizer()
        tfidf_matrix = vec.fit_transform(movies["genres"])

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        idx_mapper = pd.Series(movies.index, index=movies['movieId'])

        def predict(id):
            logging.debug("predicting for {id}".format(id=id))
            index = idx_mapper[id]
            sim_scores = list(enumerate(cosine_sim[index]))
            sim_scores_sorted = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            movie_ids = idx_mapper.iloc[[i[0] for i in sim_scores_sorted]].index.tolist()
            scores = [i[1] for i in sim_scores_sorted]

            return list(zip(movie_ids, scores))[:MAX_RECOMMENDATIONS]

        recommendations = []

        for index in idx_mapper.index.tolist():
            for r in predict(index):
                if index == r[0]:
                    continue
                recommendations.append([index, r[0], r[1]])

        with open("data/ml/csv/TfidfGenres.csv", "w") as csv_file:
            writer = csv.writer(csv_file,
                                delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)

            writer.writerows(recommendations)

    def upload(self):
        with open("data/ml/csv/TfidfGenres.csv", "r") as csv_file:
            recommendations = []
            reader = csv.reader(csv_file,
                                delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)

            for i, line in enumerate(reader):
                r = common.Recommendation(**{"engine_name": "TfidfGenres",
                                             "source_product_id": line[0],
                                             "recommended_product_id": line[1],
                                             "score": line[2]})
                recommendations.append(r)

                if i % 10000 == 0:
                    utils.insert(recommendations, db_host=DB_HOST)
                    del recommendations[:]


class TopRated(QueryBasedEngine):
    def __init__(self):
        super(TopRated, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Product)

        if context.user:
            recommendations = recommendations.filter(notflix.Product.genres.contains(context.user.favorite_genres))

        recommendations = recommendations \
            .order_by(notflix.Product.rating.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS).all()

        return recommendations


class MostRecent(QueryBasedEngine):
    def __init__(self):
        super(MostRecent, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(notflix.Product)

        if context.user:
            recommendations = recommendations.filter(notflix.Product.genres.contains(context.user.favorite_genres))

        recommendations = recommendations.order_by(notflix.Product.year.desc().nullslast()) \
                                         .limit(MAX_RECOMMENDATIONS).all()

        return recommendations
