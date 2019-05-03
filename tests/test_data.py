import unittest
from src.web import create_app
from src.data_interface import Cache, model

cache = Cache()
app = create_app()

with app.app_context():
    model.init()


class TestRedis(unittest.TestCase):
    def test_up(self):
        cache.redis_cache.ping()

    def test_set(self):
        cache.set("test:set", "foo")
        self.assertEqual(cache.get("test:set"), b"foo")

    def test_append(self):
        cache.append("test:list", "one")
        cache.append("test:list", "two")

        cache.get("test:list", start=0, end=-1)


class TestPostgres(unittest.TestCase):
    def test_up(self):
        with app.app_context():
            model.db.session.execute('SELECT 1')
