import os
import logging

# paths
DATASETS_PATH = os.path.abspath("datasets")
ML_PATH = os.path.abspath("src/ml")

# data.cache
CACHE_HOST = "redis"
CACHE_TIMEOUT = 30

# data.db
DB_HOST = "postgresql://{user}:{password}@{host}/{db}".format(
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    db=os.environ.get("POSTGRES_DB"),
    host=os.environ.get("HOST")
)

# recommender
MAX_RECOMMENDATIONS = 25
BATCH_UPLOAD_SIZE = 50000

# logging
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename="notflix.log")
formatter = logging.Formatter(
    "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
