import os

# paths
DATASETS_PATH = os.path.abspath("../datasets")
ML_PATH = os.path.abspath("../ml")

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
