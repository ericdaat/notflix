import pandas as pd
from gensim.models import Word2Vec

# Dataset

dataset = pd.read_csv("netflix_dataset.csv", header=None)
dataset.columns = ["movie_id", "user_id", "rating", "date"]

dataset["movie_id"] = dataset["movie_id"].astype(str)
corpus = dataset[dataset.rating > 3]\
            .groupby("user_id")["movie_id"]\
            .apply(list).tolist()
del dataset

# Model

m = Word2Vec()

m.build_vocab(corpus)

m.train(corpus,
        total_examples=m.corpus_count,
        epochs=4)

m.save('../src/bin/word2vec.pkl')

Word2Vec.load('../src/bin/word2vec.pkl')
