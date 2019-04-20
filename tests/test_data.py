import unittest
from src.data import Cache
from src.data.model import engine

cache = Cache()

class TestRedis(unittest.TestCase):
    def test_up(self):
        cache.redis_cache.ping()


class TestPostgres(unittest.TestCase):
    def test_up(self):
        engine.connect()
