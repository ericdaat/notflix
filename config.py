import os
from src.utils.logging import setup_logging

# paths
DATASETS_PATH = os.path.abspath("./datasets")
ML_PATH = os.path.abspath("./models")

# data.cache
CACHE_HOST = os.environ.get("REDIS_HOST")
CACHE_TIMEOUT = 30

# data.db
DB_HOST = "postgresql://{user}:{password}@{host}/{db}".format(
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    db=os.environ.get("POSTGRES_DB"),
    host=os.environ.get("POSTGRES_HOST")
)

# recommender
MAX_RECOMMENDATIONS = 25
BATCH_UPLOAD_SIZE = 50000

# logging
setup_logging(config_path="logging.yml")
