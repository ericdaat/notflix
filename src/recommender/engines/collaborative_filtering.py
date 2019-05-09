import os
import pandas as pd
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
from gensim.models import Word2Vec, KeyedVectors

from src.recommender.engines import OfflineEngine, OnlineEngine
from src.utils.data import (
    matrix_from_df_with_vect, recommendations_from_similarity_matrix
)
from config import MAX_RECOMMENDATIONS, DATASETS_PATH, ML_MODELS_PATH


class ItemBasedCF(OfflineEngine):
    def __init__(self):
        super(ItemBasedCF, self).__init__()
        self.input_id_kind = "item"

    def train(self):
        logging.info("training {0}".format(self.type))

        df = pd.read_csv(
            os.path.join(DATASETS_PATH, "movielens", "ml-1m", "ratings.csv")
        )

        v = CountVectorizer(token_pattern="[0-9]+")
        v.fit(df["movieId"].astype(str))

        X, movie_ids = matrix_from_df_with_vect(df, "movieId", "userId", v)

        cosine_sim = 1 - pairwise_distances(X, metric="cosine")

        recommendations = recommendations_from_similarity_matrix(
            movie_ids=movie_ids,
            sim_matrix=cosine_sim,
            n_recommendations=MAX_RECOMMENDATIONS,
            input_kind=self.input_id_kind
        )

        self.save_recommendations_to_csv(recommendations)


class Item2Vec(OfflineEngine):
    def __init__(self):
        super(Item2Vec, self).__init__()
        self.input_id_kind = "item"

    def train(self):
        logging.info("training {0}".format(self.type))

        df = pd.read_csv(
            os.path.join(DATASETS_PATH, "movielens", "ml-1m", "ratings.csv")
        )

        corpus = df[["userId", "movieId"]]\
            .astype(str)\
            .groupby("userId")["movieId"]\
            .apply(list).tolist()

        model = Word2Vec(
            min_count=0,
            window=10,
            size=100
        )

        model.build_vocab(corpus)

        model.train(
            corpus,
            total_examples=model.corpus_count,
            epochs=20
        )

        recommendations = []

        for movie_id in model.wv.index2word:
            neighbors = model.wv.most_similar(
                movie_id,
                topn=MAX_RECOMMENDATIONS
            )

            for neighbor_movie_id, score in neighbors:
                recommendations.append([
                    int(movie_id),
                    int(neighbor_movie_id),
                    self.input_id_kind,
                    score
                ])

        self.save_recommendations_to_csv(recommendations)


class Item2VecOnline(OnlineEngine):
    def __init__(self):
        super(Item2VecOnline, self).__init__()

    def train(self):
        pass

    def load_model(self):
        model = KeyedVectors.load(
            os.path.join(ML_MODELS_PATH, "bin", "Item2Vec.bin"),
            mmap='r'
        )

        return model

    def predict(self, context):
        if context.history:
            items = filter(
                lambda x: x in self.model.vocab,
                [str(item) for item in context.history]
            )
        else:
            items = []

        try:
            neighbors = self.model.most_similar(
                items,
                topn=MAX_RECOMMENDATIONS
            )
        except ValueError:
            neighbors = []

        ids = [n[0] for n in neighbors]
        scores = [n[1] for n in neighbors]

        return ids, scores
