import os
import pandas as pd
import sqlite3
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from web.models import Movie, Rating
import csv
import pprint


base_dir = 'C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\csv'
db_path = 'C:\\Users\\maria\\PycharmProjects\\movie_rec\\db.sqlite3'


# Load dataset into pandas dataFrame
def load_dataset():

    print("Loading Dataset")

    df_movies = pd.read_csv(os.path.join(base_dir, 'movie.csv'))
    df_movie_ratings = pd.read_csv(os.path.join(base_dir, 'rating.csv'))

    genome_scores = pd.read_csv(os.path.join(base_dir, 'genome_scores.csv'))
    genome_tags = pd.read_csv(os.path.join(base_dir, 'genome_tags.csv'))

    return df_movies, df_movie_ratings, genome_scores, genome_tags


# Join movie tags as one single string
def concatenate_tags(tags):
    tags_as_str = ' '.join(set(tags))
    return tags_as_str


def calculate_similarity(genome_scores, genome_tags, movies, movie_ratings):
    tf_idf = TfidfVectorizer()

    # relevant_tags = genome_scores[genome_scores.relevance > 0.3][['movieId', 'tagId']]
    movie_tags = pd.merge(genome_scores, genome_tags, on='tagId', how='left')[['movieId', 'tagId']]
    movie_tags['tagId'] = movie_tags.tagId.astype(str)

    print(movie_tags)

    tags_per_movie = movie_tags.groupby('movieId')['tagId'].agg(movie_tags=concatenate_tags).reset_index()

    avg_movie_ratings = calculate_ratings(movie_ratings)

    movies_with_ratings = pd.merge(movies, avg_movie_ratings, on='movieId')
    dataset = pd.merge(movies_with_ratings, tags_per_movie, on='movieId', how='left')

    dataset.rename(columns={'movieId': 'movie_id'}, inplace=True)

    movies_with_tags = dataset.movie_tags.notnull()
    movies_without_ratings = dataset.movie_tags.isnull()
    dataset_with_tags = dataset[movies_with_tags].reset_index(drop=True)
    uncomparable_movies = dataset[(~movies_with_tags) | (movies_without_ratings)]

    print("calculating movie to movie similarity...")

    vectorized = tf_idf.fit_transform(dataset_with_tags.movie_tags)
    m2m_matrix = pd.DataFrame(cosine_similarity(vectorized))
    index = dataset_with_tags['movie_id']
    m2m_matrix.columns = [str(index[int(col)]) for col in m2m_matrix.columns]
    m2m_matrix.index = [index[idx] for idx in m2m_matrix.index]
    m2m_similarity = m2m_matrix.stack().reset_index()
    m2m_similarity.columns = ['first_movie_id', 'second_movie_id', 'similarity_score']
    return m2m_similarity, dataset_with_tags, uncomparable_movies


def calculate_ratings(movie_ratings):
    avg_ratings = movie_ratings.groupby('movieId').agg(
        rating_mean=('rating', 'mean'),
        rating_median=('rating', 'median'),
        num_ratings=('rating', 'size')
    ).reset_index()
    return avg_ratings


# Write data into the database tables
def write_database(df, table_name, db_connection):
    total_length = len(df)
    step = int(total_length / 100)

    with tqdm(total=total_length) as pbar:
        for i in range(0, total_length, step):
            subset = df[i: i + step]
            subset.to_sql(table_name, db_connection, if_exists='append', index=False)
            pbar.update(step)


# Initiate database tables with column names and initiate filling of database tables
def fill_database(movie_to_movie_similarity, dataset_with_tags, uncomparable_movies):
    dataset_col_order = ['movie_id', 'title', 'genres', 'num_ratings', 'rating_median', 'rating_mean', 'comparable']
    dataset_with_tags['comparable'] = True
    uncomparable_movies['comparable'] = False

    print("writing movies with tags to CSV...")
    print(dataset_with_tags)
    output_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\movie.csv"
    dataset_with_tags.to_csv(output_file, index=False)


    print("writing movies without tags to CSV...")
    print(uncomparable_movies)
    output_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\movie_without_tag.csv"
    uncomparable_movies.to_csv(output_file, index=False)

    print("writing movie similarities to CSV...")
    print(movie_to_movie_similarity)
    output_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\similarity.csv"
    movie_to_movie_similarity.to_csv(output_file, index=False)


def main():
    # get data
    movies, movie_ratings, genome_scores, genome_tags = load_dataset()
    # connect to database for write data similarity
    db_connection = sqlite3.connect(db_path)

    movie_to_movie_similarity, dataset_with_tags, uncomparable_movies = calculate_similarity(genome_scores, genome_tags,
                                                                                             movies, movie_ratings)

    fill_database(movie_to_movie_similarity, dataset_with_tags, uncomparable_movies)


if __name__ == "__main__":
    main()
