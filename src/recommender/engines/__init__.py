"""This is the ``engines`` package, where we define the
recommendation engines.

This package contains the following modules:

- ``engine``: Module where the base classes are defined. All the created
    engines should inherit from one of these base classes. They define the
    skeleton of the engine, like which methods they must overwrite.
- ``collaborative_filtering``: All collaborative filtering engines
- ``content_based``: All content based filtering engines
- ``generic``: All the generic engines, that are not really collaborative
    or content based (e.g display the most popular items, or the items
    in the user browsing history, etc ...)
"""

from src.recommender.engines.engine import OfflineEngine, OnlineEngine
from src.recommender.engines.collaborative_filtering import *
from src.recommender.engines.content_based import *
from src.recommender.engines.generic import *
