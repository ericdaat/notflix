import logging
from gensim.models import Word2Vec
from application.engines.engine import Engine
from data.db import get_session
from data.db import Product as ProductTable


class MLBasedEngine(Engine):
    def __init__(self):
        super(MLBasedEngine, self).__init__()
        self.model = Word2Vec.load('data/ml/bin/word2vec.pkl')

    def recommend(self, active_product):
        r = super(MLBasedEngine, self).recommend(active_product)

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
