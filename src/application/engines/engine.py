from abc import ABC, abstractmethod
import logging

from application.templates.recommendations import Recommendations
from data_connector.models import Engine as EngineTable
from data_connector.utils import get_session


class Engine(ABC):
    def __init__(self):
        self.type = type(self).__name__
        logging.debug("Creating instance of {0}".format(self.type))

    @abstractmethod
    def recommend(self, active_product):
        r = Recommendations()
        r.type = self.type

        session = get_session()

        name, priority = session.query(EngineTable.display_name,
                                       EngineTable.priority)\
                                .filter(EngineTable.type == self.type)\
                                .one()

        r.display_name = name
        r.priority = priority

        return r

    @abstractmethod
    def update(self):
        return
