import logging
from application.engines.engine import Engine
from data_connector.utils import get_session
from data_connector.models import Product as ProductTable


class DBBasedEngine(Engine):
    def __init__(self):
        super(DBBasedEngine, self).__init__()

    def recommend(self, active_product):
        r = super(DBBasedEngine, self).recommend(active_product)

        s = get_session()
        recommendations = s.query(ProductTable)\
                           .filter(ProductTable.genres == active_product.genres)\
                           .filter(ProductTable.id != active_product.id)\
                           .limit(10).all()

        r.products = recommendations
        r.display_name = r.display_name.format(active_product.name)  # dynamic name

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        pass
