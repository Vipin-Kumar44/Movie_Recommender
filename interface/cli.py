from services.recommender import ContentBasedRecommender
from services.tmdb_service import TMDBService
from utils.data_loader import load_and_preprocess_data

def display_recommendations(recommendations):
    """Display recommendations in CLI"""
    if recommendations is None or recommendations.empty:
        print("No recommendations found.")
        return
    
    print("\nRecommended Movies:")
    print("=" * 50)
    for idx, row in recommendations.iterrows():
        poster_url = TMDBService.get_movie_poster_url(row['poster_path'])
        print(f"\nTitle: {row['title']}")
        print(f"Rating: {row['vote_average']}/10")
        if poster_url:
            print(f"Poster URL: {poster_url}")
    print("=" * 50)

def run_cli():
    """Run the command line interface"""
    print("Movie Recommendation System")
    print("=" * 50)
    
    # Load data and initialize recommender
    movies_df = load_and_preprocess_data()
    recommender = ContentBasedRecommender(movies_df)
    
    while True:
        print("\nOptions:")
        print("1. Get recommendations by movie title")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            title = input("Enter a movie title: ")
            min_rating = float(input("Minimum rating (0-10, 0 for no filter): "))
            recommendations = recommender.recommend(title, min_rating=min_rating)
            display_recommendations(recommendations)
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")