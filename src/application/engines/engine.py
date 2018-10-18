from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.templates.recommendations import Recommendations
from application.data_connector.db import Engine as DBEngine


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__

    @abstractmethod
    def recommend(self, context=None):
        r = Recommendations()
        r.type = self.type
        r.ids = []
        r.scores = []

        engine = create_engine("mysql://root@localhost/recommender")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        name, priority = session.query(DBEngine.display_name,
                                       DBEngine.priority)\
                                .filter(DBEngine.type == self.type)\
                                .one()

        r.display_name = name
        r.priority = priority

        return r

    @abstractmethod
    def update(self):
        return
