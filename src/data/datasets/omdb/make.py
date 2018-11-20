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
        output.write("\n")
        with open(os.path.join('..', 'movielens', 'raw', 'movies.csv'), 'r', encoding='latin1') as input:
            
            reader = csv.reader(input, delimiter=',', quotechar='"')
            
            for i, (id, name, genres) in enumerate(reader):
                match = re.search('\(([0-9]{4})\)', name)
                year = match.group(1) if match else None
                name = name.split(',')[0].strip()
                name = name.split('(')[0].strip()

                params = {"t": name, "apikey": api_key}
                if year:
                    params["year"] = year

                movie_json = requests.get(url=url, params=params).json()
                
                movie_json["id"] = id

                if eval(movie_json["Response"]):
                    output.write(json.dumps(movie_json) + "\n")
                    print("got movie {0}".format(name))
                else:
                    print("failed for movie {0}, at index {1}".format(name, i))


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
