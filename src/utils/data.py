import pandas as pd
from scipy.sparse import csr_matrix


def sparse_matrix_from_df(df, groupby, indicator):
    """ Make a scipy sparse matrix from a pandas Dataframe

    Args:
        df (pd.DataFrame): Dataframe with the matrix desired rows as index
        groupby (str): Name of the column to set as matrix column
        indicator (str): Name of the column that will serve as data

    Returns:
        sparse matrix (scipy.sparse.csr_matrix)
        row values (list)
        column values (list)

    """
    rows_u = list(df.index.unique())
    columns_u = list(df[groupby].unique())

    data = df[indicator].tolist()

    row = pd.Series(df.index) \
        .astype("category", categories=rows_u) \
        .cat.codes
    col = df[groupby] \
        .astype("category", categories=columns_u) \
        .cat.codes

    sparse_matrix = csr_matrix((data, (row, col)),
                               shape=(len(rows_u), len(columns_u)))

    return sparse_matrix, rows_u, columns_u


def matrix_from_df_with_vect(df, groupby_column, data_column, vectorizer):
    grouped_df = df.groupby(groupby_column)
    group_keys = list(grouped_df.groups.keys())

    data = grouped_df[data_column]\
        .apply(list)\
        .apply(lambda r: " ".join(list(map(str, r))))\
        .tolist()

    return vectorizer.transform(data), group_keys
