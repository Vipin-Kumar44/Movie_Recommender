import pytest
import pandas as pd
from unittest.mock import patch
from services.recommender import ContentBasedRecommender

# Sample test data
@pytest.fixture
def sample_movies_df():
    return pd.DataFrame({
        'title': ['The Avengers', 'Iron Man', 'Thor', 'Captain America', 'Guardians of the Galaxy'],
        'content_features': [
            'superhero team shield avenger',
            'superhero iron man suit',
            'superhero norse god hammer',
            'superhero world war shield',
            'space superhero team raccoon tree'
        ],
        'vote_average': [8.0, 7.9, 7.0, 6.9, 8.1]
    })

def test_recommendations_with_exact_match(sample_movies_df):
    """Test that recommendations are returned for an exact title match"""
    recommender = ContentBasedRecommender(sample_movies_df)
    recommendations = recommender.recommend('The Avengers')
    
    assert recommendations is not None
    assert len(recommendations) > 0
    assert 'The Avengers' not in recommendations['title'].values  # Should not recommend itself

def test_recommendations_with_fuzzy_match(sample_movies_df):
    """Test that fuzzy matching works for slightly misspelled titles"""
    recommender = ContentBasedRecommender(sample_movies_df)
    
    # Test various misspellings
    for misspelled in ['Avengrs', 'Aven', 'The Aven']:
        recommendations = recommender.recommend(misspelled)
        assert recommendations is not None
        assert len(recommendations) > 0

def test_no_recommendations_for_unknown_title(sample_movies_df):
    """Test that None is returned for unknown titles"""
    recommender = ContentBasedRecommender(sample_movies_df)
    recommendations = recommender.recommend('Unknown Movie 123')
    assert recommendations is None

def test_recommendations_with_rating_filter(sample_movies_df):
    """Test that rating filter works correctly"""
    recommender = ContentBasedRecommender(sample_movies_df)
    
    # Get recommendations with minimum rating of 7.5
    recommendations = recommender.recommend('The Avengers', min_rating=7.5)
    
    assert recommendations is not None
    assert all(recommendations['vote_average'] >= 7.5)
    assert len(recommendations) <= 4  # Should be less than unfiltered

def test_recommendation_quality(sample_movies_df):
    """Test that recommendations are actually similar"""
    recommender = ContentBasedRecommender(sample_movies_df)
    
    # For a superhero movie, we should get other superhero movies
    recommendations = recommender.recommend('Iron Man')
    assert all('superhero' in feat for feat in recommendations['content_features'])

def test_number_of_recommendations(sample_movies_df):
    """Test that we get exactly N recommendations when requested"""
    recommender = ContentBasedRecommender(sample_movies_df)
    
    for n in [1, 3, 5]:
        recommendations = recommender.recommend('Thor', n=n)
        assert len(recommendations) == min(n, len(sample_movies_df)-1)  # Can't recommend more than available

@patch('services.recommender.get_close_matches')
def test_title_matching_mechanism(mock_fuzzy, sample_movies_df):
    """Test the title matching logic"""
    mock_fuzzy.return_value = ['The Avengers']  # Force a match
    
    recommender = ContentBasedRecommender(sample_movies_df)
    recommendations = recommender.recommend('Any Title')
    
    mock_fuzzy.assert_called_once()
    assert recommendations is not None

def test_empty_dataframe_handling():
    """Test that the recommender handles empty data gracefully"""
    with pytest.raises(ValueError):
        ContentBasedRecommender(pd.DataFrame())

def test_missing_columns_handling():
    """Test that missing required columns raise an error"""
    with pytest.raises(KeyError):
        ContentBasedRecommender(pd.DataFrame({'wrong_column': []}))