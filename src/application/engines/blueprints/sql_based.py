import logging
from application.engines.engine import Engine


class SQLBasedEngine(Engine):
    def __init__(self):
        super(SQLBasedEngine, self).__init__()

    def recommend(self, context):
        r = super(SQLBasedEngine, self).recommend(context)
        # session = get_session()
        # products = session.query(Product).limit(5).all()

        r.ids = [1, 2, 3]
        r.scores = [0.9, 0.7, 0.4]

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        return
