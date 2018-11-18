import re
from collections import defaultdict
from glob import glob
import csv

with open("netflix_dataset.csv", "a") as output:
    writer = csv.writer(output,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL)
    
    for filename in glob("netflix/combined_data_*.txt"):
        print(filename)

        movie_id = None
        data = []

        with open(filename, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if re.match(pattern=r"^[0-9]+:$", string=line):
                movie_id = line.split(":")[0]
                continue

            user_id, rating, date = line.strip().split(",")

            data.append((movie_id, user_id, rating, date))
        
        writer.writerows(data)
        del data