import logging
from application.engines.engine import Engine


class FirstEngine(Engine):
    def __init__(self):
        super(FirstEngine, self).__init__()

    def recommend(self):
        r = super(FirstEngine, self).recommend()

        logging.debug(r.to_string())

        return r.to_dict()
