import unittest
from src.data_interface import Cache, model, engine

cache = Cache()
model.init()


class TestRedis(unittest.TestCase):
    def test_up(self):
        cache.redis_cache.ping()


class TestPostgres(unittest.TestCase):
    def test_up(self):
        engine.connect()
