import pandas as pd
from gensim.models import Word2Vec


def main():
    # Dataset
    dataset = pd.read_csv("../datasets/movielens/raw/ratings.csv")

    dataset["movieId"] = dataset["movieId"].astype(str)
    corpus = dataset[dataset["rating"] > 3].groupby("userId")["movieId"].apply(list).tolist()
    del dataset

    # Model
    m = Word2Vec()
    m.build_vocab(corpus)
    m.train(corpus,
            total_examples=m.corpus_count,
            epochs=4)
    m.save('./bin/word2vec.pkl')


if __name__ == "__main__":
    main()
