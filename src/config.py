import os

# data.cache
CACHE_HOST = "redis"
CACHE_TIMEOUT = 30

# data.db
DB_HOST = "postgresql://{user}:{password}@{host}/{db}".format(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db=os.environ["POSTGRES_DB"],
    host=os.environ["HOST"]
)

# recommender
MAX_RECOMMENDATIONS = 25
