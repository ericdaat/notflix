import logging
from application.engines.engine import Engine
from application.data_connector.cache import Cache


class CacheBasedEngine(Engine):
    def __init__(self):
        super(CacheBasedEngine, self).__init__()
        self.cache = Cache()

    def make_cache_key(self, context):
        cache_key = "{0}-{1}".format(self.type, context.item_id)

        return cache_key

    def recommendation_from_cache(self, key, recommendation):
        value = self.cache.get(key)

        if value:
            value = eval(value)
            assert isinstance(value, list)
            recommendation.ids = [v[0] for v in value]
            recommendation.scores = [v[1] for v in value]

        return recommendation

    def recommend(self, context):
        r = super(CacheBasedEngine, self).recommend(context)

        cache_key = self.make_cache_key(context)
        r = self.recommendation_from_cache(cache_key, r)

        logging.debug(r.to_string())

        return r.to_dict()

    def update(self):
        return
