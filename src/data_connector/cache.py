from redis import StrictRedis
from config import CACHE_TIMEOUT, CACHE_HOST


class Cache(object):
    def __init__(self):
        self.redis_cache = StrictRedis(host=CACHE_HOST)
        self.ex = CACHE_TIMEOUT

    def get(self, key):
        """ Get an object from cache by its key
        :param str key: cache key
        :return: cached object
        :rtype: str
        """
        return self.redis_cache.get(key)

    def set(self, key, value):
        """ Set an object in cache by its key
        :param str key: cache key
        :param str value: object to store in cache
        :return: None
        """
        return self.redis_cache.set(key, value, ex=self.ex)
