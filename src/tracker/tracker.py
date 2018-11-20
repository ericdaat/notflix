import logging
from data.cache import Cache


class Tracker(object):
    def __init__(self):
        self.cache = Cache()

    def store_item_viewed(self, key, item):
        logging.debug("tracking item viewed for key {0}".format(key))
        return self.cache.append(key, item)

    def get_views_history(self, key, n):
        history = self.cache.get(key, start=0, end=n-1)
        history_set = set(history)

        return history_set
