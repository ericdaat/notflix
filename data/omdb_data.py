import os
import requests
import re
import json

from data_connector.models import Product
from data_connector.utils import insert_in_db

UPPER_BOUND = 500
LOWER_BOUND = 22
OUTPUT_FILE = "data.txt"


def get_data_from_omdb(api_key):
    with open(OUTPUT_FILE, 'a') as output:
        output.write("\n")
        with open(os.path.join('ml-1m', 'movies.dat'), 'r', encoding='latin1') as input:
            for i, line in enumerate(input.readlines()):
                if i < LOWER_BOUND + 1:
                    continue
                elif i > UPPER_BOUND:
                    break

                line = line.split('::')
                id = line[0]
                name = line[1]
                genres = line[2].strip()
                match = re.search('\(([0-9]{4})\)', name)
                year = match.group(1) if match else None

                url = 'http://www.omdbapi.com/?t={0}&y={1}&apikey={2}'
                movie_json = requests.get(url.format(name.split('(')[0].strip(), year, api_key)).json()
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
                 "year": None}

            product = Product(**d)
            ds.append(product)

        insert_in_db(ds)


if __name__ == "__main__":
    pass
    with open('ombdb.key') as f:
        api_key = f.read().strip()
    # get_data_from_omdb(api_key)
    # insert_data_to_db()
