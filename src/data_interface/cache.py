from redis import StrictRedis
from config import CACHE_TIMEOUT, CACHE_HOST


class Cache(object):
    def __init__(self):
        self.redis_cache = StrictRedis(host=CACHE_HOST)
        self.ex = CACHE_TIMEOUT

    def get(self, key, start=None, end=None):
        """ Get an object from cache by its key

        Args:
            key (str): cache key
            start (int): when querying a redis list,\
                starting range of the list.
            end (int): when querying a redis list, ending range of the list.

        Returns:
            str: cached object
        """

        if not (start is None or end is None):
            result = self.redis_cache.lrange(key, start=start, end=end)
        else:
            result = self.redis_cache.get(key)

        return result

    def set(self, key, value):
        """ Set an object in cache by its key

        Args:
            key (str): cache key
            value (str): object to store in cache
        """
        return self.redis_cache.set(key, value, ex=self.ex)

    def append(self, key, value):
        """ Append to a redis list

        Args:
            key (str): cache key
            value (str): object to store in cache
        """
        return self.redis_cache.lpush(key, value)
