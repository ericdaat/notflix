import logging
from application.engines.engine import Engine


class FirstEngine(Engine):
    def __init__(self):
        super(FirstEngine, self).__init__()

    def recommend(self, context=None):
        r = super(FirstEngine, self).recommend(context)

        cache_key = "{0}-{1}".format(self.name, context.item_id)
        r = self.recommendation_from_cache(cache_key, r)

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        return
