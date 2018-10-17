import logging
from redis import StrictRedis
from application.config import CACHE_TIMEOUT, CACHE_HOST


class Cache(object):
    def __init__(self):
        self.redis_cache = StrictRedis(host=CACHE_HOST)
        self.ex = CACHE_TIMEOUT
        logging.debug("initialized cache.")

    def get(self, key):
        self.redis_cache.get(key)

    def set(self, key, value):
        self.redis_cache.set(key, value, ex=self.ex)
