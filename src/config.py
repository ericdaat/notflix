import os

# data.cache
CACHE_HOST = "redis"
CACHE_TIMEOUT = 30

# data.db
DB_HOST = "mysql://{user}:{password}@{host}/{db}".format(
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    db=os.environ.get("MYSQL_DATABASE"),
    host=os.environ.get("MYSQL_HOST")
)

# recommender
MAX_RECOMMENDATIONS = 25
