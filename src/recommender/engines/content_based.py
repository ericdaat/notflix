import os
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy import sparse
from config import MAX_RECOMMENDATIONS, DATASETS_PATH, ML_MODELS_PATH
from src.recommender.engines.engine import (
    QueryBasedEngine, OfflineEngine
)
from src.data_interface import model


class SameGenres(QueryBasedEngine):
    def __init__(self):
        super(SameGenres, self).__init__()

    def compute_query(self, session, context):
        recommendations = session\
            .query(model.Movie)\
            .filter(model.Movie.genres.contains(
                [g[0] for g in context.item.genres]))\
            .filter(model.Movie.id != context.item.id) \
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations


class OneHotMultiInput(OfflineEngine):
    def __init__(self):
        super(OneHotMultiInput, self).__init__()

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
        # read dataset
        df = pd.read_json(
            os.path.join(DATASETS_PATH, "movielens", "omdb.csv"),
            lines=True
        )

        # select features
        movies = df[[
            "id", "Title", "Plot", "Country", "Actors", "Director",
            "Production", "Genre", "Language", "Released", "imdbVotes",
            "imdbRating"
        ]]

        # edit features
        movies.replace("N/A", np.nan, inplace=True)
        movies["Released_year"] = movies["Released"]\
            .fillna("")\
            .str.split(" ").str[-1]\
            .replace("", 0).astype(int)
        movies["Released_decade"] = pd.cut(
            movies["Released_year"],
            range(1920, 2020, 10)
        )
        movies["imdbVotes"] = movies["imdbVotes"]\
            .str.replace(",", "").fillna(0).astype(int)
        movies["popularity"] = pd.cut(movies["imdbVotes"], 10)

        # init vectorizers
        country_vect = CountVectorizer()
        director_vect = CountVectorizer()
        genre_vect = CountVectorizer()
        language_vect = CountVectorizer()
        plot_vect = TfidfVectorizer(min_df=2, max_df=0.5)
        title_vect = TfidfVectorizer(min_df=2, max_df=0.5)

        # fit vectorizers and concatenate
        X = sparse.hstack([
            country_vect.fit_transform(movies["Country"].fillna("")),
            genre_vect.fit_transform(movies["Genre"].fillna("")),
            language_vect.fit_transform(movies["Language"].fillna("")),
            director_vect.fit_transform(movies["Director"].fillna("")),
            pd.get_dummies(movies["Released_decade"]).values,
            plot_vect.fit_transform(movies["Plot"].fillna("")),
            title_vect.fit_transform(movies["Title"].fillna("")),
        ])

        # fit model
        nbrs = NearestNeighbors(
            n_neighbors=MAX_RECOMMENDATIONS,
            metric="cosine"
        )
        nbrs.fit(X)

        distances, neighbors = nbrs.kneighbors(X)

        # compute recommendations
        to_insert = []

        for index, movie_id in enumerate(movies.id):
            scores = 1. - distances[index]
            recommendations = map(lambda r: movies.id[r], neighbors[index])

            for score, recommended_movie_id in zip(scores, recommendations):
                if movie_id == recommended_movie_id:
                    continue

                to_insert.append([
                    movie_id,
                    recommended_movie_id,
                    "item",
                    score])

        # export recomemndations as CSV
        output_filepath = os.path.join(ML_MODELS_PATH, "csv", self.type + ".csv")
        with open(output_filepath, "w") as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerows(to_insert)


class TfidfGenres(OfflineEngine):
    def __init__(self):
        super(TfidfGenres, self).__init__()

    def train(self):
        pass


class TopRated(QueryBasedEngine):
    def __init__(self):
        super(TopRated, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(model.Movie)

        if context.user and context.user.favorite_genres:
            query_filter = model.Movie.genres\
                .contains(context.user.favorite_genres)
            recommendations = recommendations.filter(query_filter)

        recommendations = recommendations \
            .order_by(model.Movie.rating.desc().nullslast()) \
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations


class MostRecent(QueryBasedEngine):
    def __init__(self):
        super(MostRecent, self).__init__()

    def compute_query(self, session, context):
        recommendations = session.query(model.Movie)

        if context.user and context.user.favorite_genres:
            query_filter = model.Movie.genres\
                .contains(context.user.favorite_genres)
            recommendations = recommendations.filter(query_filter)

        recommendations = recommendations\
            .order_by(model.Movie.year.desc().nullslast())\
            .limit(MAX_RECOMMENDATIONS)\
            .all()

        return recommendations
