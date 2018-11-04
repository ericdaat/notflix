import logging
from data_connector.cache import Cache


class Tracker(object):
    def __init__(self):
        self.cache = Cache()

    def store_item_viewed(self, key, item):
        logging.debug("tracking item viewed for key {0}".format(key))
        return self.cache.append(key, item)

    def get_views_history(self, key, n):
        return self.cache.get(key, start=0, end=n-1)

