import logging
from gensim.models import Word2Vec
from application.engines.engine import Engine, OfflineEngine
from data.db import get_session
from data.db import Product as ProductTable


class Word2Vec(Engine):
    def __init__(self):
        super(Word2Vec, self).__init__()
        self.model = Word2Vec.load('data/ml/bin/word2vec.pkl')

    def recommend(self, active_product):
        r = super(Word2Vec, self).recommend(active_product)

        recommendations = self.model.most_similar(str(active_product.id))
        ids = [r[0] for r in recommendations]
        s = get_session()
        recommendations = s.query(ProductTable) \
            .filter(ProductTable.id.in_(ids)) \
            .filter(ProductTable.id != active_product.id) \
            .limit(10).all()

        r.products = recommendations

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        pass


class CosineMovies(OfflineEngine):
    def __init__(self):
        super(CosineMovies, self).__init__()
