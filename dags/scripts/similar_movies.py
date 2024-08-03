from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import csr_matrix, hstack

import gc

class Similarity:
    def __init__(self, loader):
        self.ratings_df = loader.get_ratings_df()
        self.users_df = loader.get_users_df()
        self.movies_df = loader.get_movies_df()
        #self.find_top_similar_movies()

    def preprocess_data(self):

        merged_df = self.ratings_df.merge(self.users_df, on='user_id')
        merged_df = merged_df.merge(self.movies_df, on='item_id')

        encoder = OneHotEncoder(sparse=False)  # Use dense array for simplicity
        demographic_features = encoder.fit_transform(merged_df[['gender', 'occupation']])

        genre_columns = ['Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary',
                         'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                         'Thriller', 'War', 'Western']
        genre_features = merged_df[genre_columns].values

        scaler = StandardScaler()
        age_features = scaler.fit_transform(merged_df[['age']])

        combined_features = hstack([csr_matrix(demographic_features), csr_matrix(age_features)])
        movie_ids = merged_df[['item_id']]

        return movie_ids, combined_features


    def calculate_similarities(self,item_features, chunk_size =1000):
        item_features_sparse = csr_matrix(item_features)
        num_items = item_features_sparse.shape[0]

        # Allocate a sparse matrix for the result
        similarity_matrix = csr_matrix((num_items, num_items))

        for start_row in range(0, num_items, chunk_size):
            end_row = min(start_row + chunk_size, num_items)
            chunk = item_features_sparse[start_row:end_row, :]
            chunk_similarity = cosine_similarity(chunk, item_features_sparse)
            similarity_matrix[start_row:end_row, :] = chunk_similarity
        return similarity_matrix

    def find_top_similar_movies(self, target_movie_titles=None, similarity_threshold=0.95):
        if target_movie_titles is None:
            target_movie_titles = []

        movie_ids, combined_features = self.preprocess_data()
        similarity_df = self.calculate_similarities(combined_features)

        # Release large objects
        del combined_features
        del similarity_df
        gc.collect()

        movie_titles = dict(zip(self.movies_df['item_id'], self.movies_df['title']))
        all_similar_movies = {}

        for target_movie_title in target_movie_titles:
            target_movie_ids = self.movies_df[self.movies_df['title'] == target_movie_title]['item_id']
            if target_movie_ids.empty:
                print(f"Target movie '{target_movie_title}' not found in the dataset.")
                continue

            target_movie_id = target_movie_ids.values[0]
            target_index = movie_ids[movie_ids['item_id'] == target_movie_id].index[0]

            similarities = {}
            for index, row in similarity_df.iterrows():
                if index == target_index:
                    continue

                similarity_score = row[target_index]
                if similarity_score >= similarity_threshold:
                    similarities[movie_ids.loc[index, 'item_id']] = similarity_score

            similar_movies = [(movie_titles[movie_id], score) for movie_id, score in similarities.items()]
            similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
            all_similar_movies[target_movie_title] = similar_movies


        for target_movie_title, similar_movies in all_similar_movies.items():
            print(f"Top similar movies to '{target_movie_title}':")
            for movie in similar_movies[:10]:
                print(f"Movie: {movie[0]}, Score: {movie[1]}")
            print()
