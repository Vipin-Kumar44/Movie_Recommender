import pandas as pd
from difflib import get_close_matches
from utils.similarity import create_tfidf_matrix, calculate_cosine_similarity

class ContentBasedRecommender:
    def __init__(self, movies_df):
        """
        Initialize the recommender with movie data
        Args:
            movies_df (pd.DataFrame): Processed movies dataframe
        """
        self.movies_df = movies_df
        self.tfidf_matrix = create_tfidf_matrix(movies_df['content_features'])
        self.cosine_sim = calculate_cosine_similarity(self.tfidf_matrix)
        self.indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

    def _get_closest_title(self, title):
        """Find closest matching title in the dataset"""
        matches = get_close_matches(title, self.movies_df['title'], n=1, cutoff=0.1)
        return matches[0] if matches else None

    def recommend(self, title, n=10, min_rating=0):
        """
        Get movie recommendations
        Args:
            title (str): Movie title to find similar movies for
            n (int): Number of recommendations to return
            min_rating (float): Minimum rating threshold
        Returns:
            pd.DataFrame: Recommended movies
        """
        closest_title = self._get_closest_title(title)
        if not closest_title:
            return None

        idx = self.indices[closest_title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar movies (skip the first one as it's the movie itself)
        movie_indices = [i[0] for i in sim_scores[1:n+1]]
        
        # Filter by minimum rating if specified
        recommendations = self.movies_df.iloc[movie_indices]
        if min_rating > 0:
            recommendations = recommendations[recommendations['vote_average'] >= min_rating]
        
        return recommendations