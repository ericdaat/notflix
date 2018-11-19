import os
import requests
import re
import json
from datetime import datetime

from data.db import Product
from data.db import insert, setup

OUTPUT_FILE = "omdb.csv"


def get_data_from_omdb(api_key):
    with open(OUTPUT_FILE, 'a') as output:
        output.write("\n")
        with open(os.path.join('..', 'netflix', 'raw', 'movie_titles.csv'), 'r', encoding='latin1') as input:
            for i, line in enumerate(input.readlines()):
                line = line.split(',')
                id = line[0]
                name = line[2]
                genres = line[2].strip()
                match = re.search('\(([0-9]{4})\)', name)
                year = match.group(1) if match else None

                url = 'http://www.omdbapi.com/?t={0}&y={1}&apikey={2}'
                movie_json = requests.get(url.format(name.split('(')[0].strip(), year, api_key)).json()
                print(movie_json)
                movie_json["id"] = id

                if eval(movie_json["Response"]):
                    output.write(json.dumps(movie_json) + "\n")


def insert_data_to_db():
    with open(OUTPUT_FILE, "r") as f:
        ds = []

        for line in f.readlines():
            movie = json.loads(line)
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
                 "duration": int(movie["Runtime"].split(" min")[0]) if movie["Runtime"] != "N/A" else None}

            product = Product(**d)
            ds.append(product)

        insert(ds)


if __name__ == "__main__":
    with open('omdb.key') as f:
        api_key = f.read().strip()
    get_data_from_omdb(api_key)
    setup()
    insert_data_to_db()
