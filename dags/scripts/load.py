import pandas as pd
import chardet
import os


class Loader:
    def __init__(self, parent_folder):
        self.parent_folder = parent_folder
        self.ratings_file_path = os.path.join(parent_folder, 'ml-100k', 'u.data')
        self.users_file_path = os.path.join(parent_folder, 'ml-100k', 'u.user')
        self.occupation_file_path = os.path.join(parent_folder, 'ml-100k', 'u.occupation')
        self.movies_file_path = os.path.join(parent_folder, 'ml-100k', 'u.item')

    def get_ratings_df(self):
        ratings_df = pd.read_csv(self.ratings_file_path, sep='\t', header=None,
                                 names=['user_id', 'item_id', 'rating', 'timestamp'])
        return ratings_df

    def get_users_df(self):
        users_df = pd.read_csv(self.users_file_path, sep='|', header=None,
                               names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
        return users_df

    def get_occupation_df(self):
        occupation_df = pd.read_csv(self.occupation_file_path, header=None, names=['occupation'])
        return occupation_df

    def get_movies_df(self):
        with open(self.movies_file_path, 'rb') as file:
            result = chardet.detect(file.read())
        movies_df = pd.read_csv(self.movies_file_path, sep='|', header=None,
                                names=['item_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown',
                                       'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime',
                                       'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                                       'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], encoding=result['encoding'])
        return movies_df
