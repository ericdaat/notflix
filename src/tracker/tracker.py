import logging
from src.data_interface.cache import Cache


class Tracker(object):
    def __init__(self):
        self.cache = Cache()

    def store_item_viewed(self, key, item):
        """ Store item viewed in cache

        Args:
            key (str): cache key
            item (str): value

        Returns:

        """
        logging.debug("tracking item {item} viewed for key {key}"
                      .format(key=key, item=item))
        return self.cache.append(key, item)

    def get_views_history(self, key, n=-1):
        history = self.cache.get(key, start=0, end=n)
        history = map(int, history)
        history_set = set(history)

        return history_set
