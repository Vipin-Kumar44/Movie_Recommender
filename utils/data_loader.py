import pandas as pd
import json
from config.settings import MOVIES_DATA_PATH, CREDITS_DATA_PATH

def load_and_preprocess_data():
    """
    Load and preprocess the movie data from CSV files
    Returns:
        pd.DataFrame: Processed movies dataframe
    """
    # Load datasets
    movies_df = pd.read_csv(MOVIES_DATA_PATH)
    credits_df = pd.read_csv(CREDITS_DATA_PATH)

    # Merge datasets
    credits_df.rename(columns={'movie_id': 'id'}, inplace=True)
    movies_df = movies_df.merge(credits_df, on='id')

    # Safe fallback for missing columns
    if 'title' not in movies_df.columns:
        movies_df['title'] = movies_df['original_title']

    if 'poster_path' not in movies_df.columns:
        movies_df['poster_path'] = ''  # Optional: provide a default image path

    # Process JSON-like columns safely
    def parse_json_column(x):
        try:
            return json.loads(x)
        except (TypeError, json.JSONDecodeError):
            return []

    movies_df['genres'] = movies_df['genres'].apply(lambda x: ' '.join([i['name'] for i in parse_json_column(x)]))
    movies_df['keywords'] = movies_df['keywords'].apply(lambda x: ' '.join([i['name'] for i in parse_json_column(x)]))
    movies_df['cast'] = movies_df['cast'].apply(lambda x: ' '.join([i['name'] for i in parse_json_column(x)[:5]]))
    movies_df['crew'] = movies_df['crew'].apply(lambda x: ' '.join([i['name'] for i in parse_json_column(x) if i.get('job') in ['Director', 'Producer']]))

    # Fill NaNs for overview and other text columns
    for col in ['overview', 'genres', 'keywords', 'cast', 'crew']:
        movies_df[col] = movies_df[col].fillna('')

    # Combine features
    movies_df['content_features'] = (
        movies_df['overview'] + ' ' +
        movies_df['genres'] + ' ' +
        movies_df['keywords'] + ' ' +
        movies_df['cast'] + ' ' +
        movies_df['crew']
    )

    # Final fill
    movies_df['content_features'] = movies_df['content_features'].fillna('')

    return movies_df[['id', 'title', 'vote_average', 'content_features', 'poster_path']]
