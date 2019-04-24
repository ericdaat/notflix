import os
import pandas as pd
import numpy as np
import logging
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from scipy import sparse

from config import MAX_RECOMMENDATIONS, DATASETS_PATH
from src.recommender.engines.engine import (
    QueryBasedEngine, OfflineEngine
)
from src.data_interface import model
from src.utils.data import recommendations_from_similarity_matrix

pd.options.mode.chained_assignment = None  # default='warn'


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
        self.input_id_kind = "item"

    def train(self):
        logging.info("training {0}".format(self.type))

        # read dataset
        df = pd.read_json(
            os.path.join(DATASETS_PATH, "movielens", "omdb.csv"),
            lines=True
        )

        # select features
        df = df[[
            "id", "Title", "Plot", "Country", "Actors", "Director",
            "Production", "Genre", "Language", "Released", "imdbVotes",
            "imdbRating"
        ]]

        # edit features
        df.replace("N/A", np.nan, inplace=True)
        df["Released_year"] = df["Released"]\
            .fillna("")\
            .str.split(" ").str[-1]\
            .replace("", 0).astype(int)
        df["Released_decade"] = pd.cut(
            df["Released_year"],
            range(1920, 2020, 10)
        )
        df["imdbVotes"] = df["imdbVotes"]\
            .str.replace(",", "").fillna(0).astype(int)
        df["popularity"] = pd.cut(df["imdbVotes"], 10)

        # init vectorizers
        country_vect = CountVectorizer()
        director_vect = CountVectorizer()
        genre_vect = CountVectorizer()
        language_vect = CountVectorizer()
        # plot_vect = TfidfVectorizer(min_df=2, max_df=0.5)
        # title_vect = TfidfVectorizer(min_df=2, max_df=0.5)

        # fit vectorizers and concatenate
        X = sparse.hstack([
            country_vect.fit_transform(df["Country"].fillna("")),
            genre_vect.fit_transform(df["Genre"].fillna("")),
            language_vect.fit_transform(df["Language"].fillna("")),
            director_vect.fit_transform(df["Director"].fillna("")),
            pd.get_dummies(df["Released_decade"]).values,
            # plot_vect.fit_transform(df["Plot"].fillna("")),
            # title_vect.fit_transform(df["Title"].fillna("")),
        ])

        cosine_sim = 1 - pairwise_distances(X, metric="cosine")

        movie_ids = df["id"].tolist()

        recommendations = recommendations_from_similarity_matrix(
            movie_ids=movie_ids,
            sim_matrix=cosine_sim,
            n_recommendations=MAX_RECOMMENDATIONS,
            input_kind=self.input_id_kind
        )

        self.save_recommendations_to_csv(recommendations)


class TfidfGenres(OfflineEngine):
    def __init__(self):
        super(TfidfGenres, self).__init__()
        self.input_id_kind = "item"

    def train(self):
        logging.info("training {0}".format(self.type))

        df = pd.read_json(
            os.path.join(DATASETS_PATH, "movielens", "omdb.csv"),
            lines=True
        )

        genre_vect = TfidfVectorizer()

        X = sparse.hstack([
            genre_vect.fit_transform(df["Genre"].fillna("")),
        ])

        cosine_sim = 1 - pairwise_distances(X, metric="cosine")

        movie_ids = df["id"].tolist()

        recommendations = recommendations_from_similarity_matrix(
            movie_ids=movie_ids,
            sim_matrix=cosine_sim,
            n_recommendations=MAX_RECOMMENDATIONS,
            input_kind=self.input_id_kind
        )

        self.save_recommendations_to_csv(recommendations)
