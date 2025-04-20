from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create_tfidf_matrix(content_features):
    """
    Create TF-IDF matrix from content features
    Args:
        content_features (pd.Series): Movie content features
    Returns:
        tfidf_matrix: TF-IDF matrix
    """
    tfidf = TfidfVectorizer(stop_words='english')
    return tfidf.fit_transform(content_features)

def calculate_cosine_similarity(tfidf_matrix):
    """
    Calculate cosine similarity matrix
    Args:
        tfidf_matrix: TF-IDF matrix
    Returns:
        cosine_sim: Cosine similarity matrix
    """
    return linear_kernel(tfidf_matrix, tfidf_matrix)