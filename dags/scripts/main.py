import pandas as pd
import numpy as np
import os

from load import Loader
from extract_data import Extracter
from similar_movies import Similarity


def find_top_rated_movies(loader, min_ratings=35, top_n=20):
    try:
        ratings_df = loader.get_ratings_df()
        movies_df = loader.get_movies_df()

        rating_counts = ratings_df['item_id'].value_counts()
        valid_movie_ids = rating_counts[rating_counts >= min_ratings].index
        filtered_ratings_df = ratings_df[ratings_df['item_id'].isin(valid_movie_ids)]
        avg_ratings = filtered_ratings_df.groupby('item_id')['rating'].mean().reset_index()
        top_movies = avg_ratings.merge(movies_df[['item_id', 'title']], on='item_id')
        top_movies = top_movies.sort_values(by='rating', ascending=False).head(top_n)
        return list(top_movies)
    except Exception as e:
        print(f"An error occurred in find_top_rated_movies: {e}")


def calculate_mean_age_per_occupation(loader):
    try:
        user_df = loader.get_users_df()
        occupation_df = loader.get_occupation_df()

        if not user_df['occupation'].astype(str).isin(occupation_df['occupation'].astype(str)).all():
            print("Warning: Some occupations in user data do not match the occupation list.")

        mean_age_per_occupation = user_df.groupby('occupation')['age'].mean().reset_index()
        print(mean_age_per_occupation)
    except Exception as e:
        print(f"An error occurred in calculate_mean_age_per_occupation: {e}")


def find_top_genres_by_occupation_and_age(loader):
    try:
        user_df = loader.get_users_df()
        ratings_df = loader.get_ratings_df()
        movies_df = loader.get_movies_df()

        bins = [20, 25, 35, 45, float('inf')]
        labels = ['20-25', '25-35', '35-45', '45+']
        user_df['age_group'] = pd.cut(user_df['age'], bins=bins, labels=labels, right=False)

        merged_df = ratings_df.merge(user_df[['user_id', 'age_group', 'occupation']], on='user_id')
        merged_df = merged_df.merge(movies_df[['item_id'] + list(movies_df.columns[5:])], on='item_id')

        genres_df = merged_df.melt(id_vars=['user_id', 'age_group', 'occupation', 'item_id', 'rating'],
                                   value_vars=movies_df.columns[5:],
                                   var_name='genre',
                                   value_name='genre_flag')

        genres_df = genres_df[genres_df['genre_flag'] == 1]

        genre_ratings = genres_df.groupby(['occupation', 'age_group', 'genre'])['rating'].mean().reset_index()
        top_genres = genre_ratings.groupby(['occupation', 'age_group']).apply(
            lambda x: x.sort_values(by='rating', ascending=False).head(1)).reset_index(drop=True)

        print(top_genres)
    except Exception as e:
        print(f"An error occurred in find_top_genres_by_occupation_and_age: {e}")


if __name__ == "__main__":
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    project_directory = os.getcwd()
    extract_folder = os.path.join(project_directory, 'ml-100k-extracted')

    extract_data = Extracter(url, project_directory, extract_folder)
    loader = Loader(extract_folder)

    top_movies = find_top_rated_movies(loader)
    calculate_mean_age_per_occupation(loader)  # Uncomment if needed
    find_top_genres_by_occupation_and_age(loader)  # Uncomment if needed

    similar_movies = Similarity(loader)
    similar_movies.find_top_similar_movies(top_movies)
