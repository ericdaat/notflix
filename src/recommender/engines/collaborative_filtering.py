from gensim import models
from recommender.engines.engine import OnlineEngine, OfflineEngine


class Word2Vec(OnlineEngine):
    def __init__(self):
        super(Word2Vec, self).__init__()

    def load_model(self):
        return models.Word2Vec.load('data/ml/bin/word2vec.pkl')

    def predict(self, active_product):
        recommendations = self.model.most_similar(str(active_product.id))
        ids = [r[0] for r in recommendations]

        return ids
