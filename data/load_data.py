import os
from data_connector.models import Product
from data_connector.utils import insert_in_db


def main():
    with open(os.path.join('data', 'ml-1m', 'movies.dat'), 'r', encoding='latin1') as f:
        products = []
        for line in f.readlines():
            line = line.split('::')
            name = line[1]
            genres = line[2].strip()

            product = Product(**{'name': name,
                                 'genres': genres})
            products.append(product)

        insert_in_db(products)


if __name__ == '__main__':
    main()