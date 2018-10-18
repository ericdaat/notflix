from redis import StrictRedis
from config import CACHE_TIMEOUT, CACHE_HOST


class Cache(object):
    def __init__(self):
        self.redis_cache = StrictRedis(host=CACHE_HOST)
        self.ex = CACHE_TIMEOUT

    def get(self, key):
        return self.redis_cache.get(key)

    def set(self, key, value):
        return self.redis_cache.set(key, value, ex=self.ex)
