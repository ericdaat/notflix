import os
import requests
import re
import json
from datetime import datetime
import csv

from data.db import Product
from data.db import insert, setup

OUTPUT_FILE = "omdb.csv"


def get_data_from_omdb(api_key):
    url = 'http://www.omdbapi.com/'

    with open(OUTPUT_FILE, 'a') as output:
        with open(os.path.join('..', 'movielens', 'raw', 'links.csv'), 'r', encoding='latin1') as input:

            reader = csv.reader(input, delimiter=',', quotechar='"')
            
            for i, (id, imdb_id, tmdb_id) in enumerate(reader):
                if i == 0:  # skip header
                    continue

                params = {"i": "tt{0}".format(imdb_id), "apikey": api_key}
                movie_json = requests.get(url=url, params=params).json()
                movie_json["id"] = id

                if eval(movie_json["Response"]):
                    output.write(json.dumps(movie_json) + "\n")
                else:
                    print("failed for movie index {0}".format(i))


def insert_data_to_db():
    with open(OUTPUT_FILE, "r") as f:
        ds = []

        for line in f.readlines():
            movie = json.loads(line)

            if movie["id"] == "movieId":
                continue

            # duration
            if re.match(pattern=r"[1-9]\sh", string=movie["Runtime"]):
                duration = int(movie["Runtime"].split(" h")[0]) * 60
            elif re.match(pattern=r"[0-9]+\smin", string=movie["Runtime"]):
                duration = int(movie["Runtime"].split(" min")[0])
            else:
                duration = None

            d = {"id": movie["id"],
                 "image": movie["Poster"],
                 "name": movie["Title"],
                 "genres": movie["Genre"],
                 "description": movie["Plot"],
                 "year": datetime.strptime(movie["Released"], "%d %b %Y") if movie["Released"] != "N/A" else None,
                 "rating": movie["imdbRating"] if movie["imdbRating"] != "N/A" else None,
                 "director": movie["Director"],
                 "actors": movie["Actors"],
                 "awards": movie["Awards"],
                 "language": movie["Language"],
                 "country": movie["Country"],
                 "duration": duration}

            product = Product(**d)
            ds.append(product)

        insert(ds)


if __name__ == "__main__":
    with open('omdb.key') as f:
        api_key = f.read().strip()
    # get_data_from_omdb(api_key)
    setup()
    insert_data_to_db()
