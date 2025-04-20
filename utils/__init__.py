"""
Movie Recommender Utilities Module

Exposes data loading and similarity calculation functions
"""

from .data_loader import load_and_preprocess_data
from .similarity import create_tfidf_matrix, calculate_cosine_similarity

__all__ = [
    'load_and_preprocess_data',
    'create_tfidf_matrix',
    'calculate_cosine_similarity'
]