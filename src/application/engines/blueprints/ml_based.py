import numpy as np
import logging
from application.engines.engine import Engine


class MLBasedEngine(Engine):
    def __init__(self):
        super(MLBasedEngine, self).__init__()

    def recommend(self, context):
        r = super(MLBasedEngine, self).recommend(context)

        r.ids = np.random.randint(100, size=10)
        r.scores = np.arange(1, 0, 100)

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        return
