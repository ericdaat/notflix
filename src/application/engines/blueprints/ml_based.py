from gensim.models import Word2Vec
from application.engines.engine import Engine
from data_connector.utils import get_session
from data_connector.models import Product as ProductTable


class MLBasedEngine(Engine):
    def __init__(self):
        super(MLBasedEngine, self).__init__()
        self.model = Word2Vec.load('bin/word2vec.pkl')

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

        return r.to_dict()

    def update(self):
        pass
