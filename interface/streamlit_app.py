import streamlit as st
from services.recommender import ContentBasedRecommender
from services.tmdb_service import TMDBService
from utils.data_loader import load_and_preprocess_data
import pandas as pd

# Configure page
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
        }
        .sidebar .sidebar-content {
            background-color: #1a1a2e;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #f8f9fa;
        }
        .stTextInput>div>div>input {
            background-color: #2d3436;
            color: white;
        }
        .movie-card {
            border-radius: 10px;
            padding: 15px;
            background-color: #1a1a2e;
            transition: transform 0.2s;
            height: 100%;
        }
        .movie-card:hover {
            transform: scale(1.03);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .rating {
            color: #f8f9fa;
            font-weight: bold;
        }
        .stSlider>div>div>div>div {
            background-color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)

def display_movie_card(movie, col):
    with col:
        card = st.container()
        with card:
            st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
            
            # Display poster (40% smaller)
            poster_url = TMDBService.get_movie_poster_url(movie['poster_path'])
            if poster_url:
                st.image(poster_url, use_column_width=True)
            
            # Movie title and rating
            st.markdown(f"<h4>{movie['title']}</h4>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='rating'>⭐ {movie['vote_average']}/10</div>", 
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_css()
    
    # Load data with progress indicator
    with st.spinner('Loading movie database...'):
        movies_df = load_and_preprocess_data()
        recommender = ContentBasedRecommender(movies_df)
    
    # Sidebar controls
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=CineMatch", use_column_width=True)
        st.header("Search Filters")
        
        # Search box with autocomplete
        search_term = st.text_input("Enter a movie title:", key="search_box")
        
        # Filters
        min_rating = st.slider(
            "Minimum Rating", 
            min_value=0.0, 
            max_value=10.0, 
            value=6.0, 
            step=0.5,
            help="Filter movies by minimum rating"
        )
        
        genre_options = ["All"] + sorted(list(set(
            genre for sublist in movies_df['genres'].str.split() 
            for genre in sublist if genre
        )))
        selected_genre = st.selectbox(
            "Filter by Genre", 
            genre_options,
            index=0
        )
        
        num_recommendations = st.slider(
            "Number of Recommendations", 
            min_value=5, 
            max_value=20, 
            value=10
        )
    
    # Main content area
    st.title("🎬 CineMatch")
    st.markdown("Discover your next favorite movie based on what you love!")
    
    if search_term:
        with st.spinner(f'Finding recommendations similar to "{search_term}"...'):
            recommendations = recommender.recommend(
                search_term, 
                n=num_recommendations,
                min_rating=min_rating
            )
        
        if recommendations is not None and not recommendations.empty:
            # Apply genre filter if selected
            if selected_genre != "All":
                recommendations = recommendations[
                    recommendations['genres'].str.contains(selected_genre)
                ]
            
            st.success(f"Found {len(recommendations)} recommendations")
            
            # Display results in responsive grid
            cols = st.columns(4)
            for idx, (_, movie) in enumerate(recommendations.iterrows()):
                display_movie_card(movie, cols[idx % 4])
        else:
            st.warning("No recommendations found. Try a different movie or adjust filters.")
    
    # Popular movies section when no search
    else:
        st.subheader("Popular This Week")
        popular_movies = movies_df.sort_values('vote_average', ascending=False).head(8)
        
        cols = st.columns(4)
        for idx, (_, movie) in enumerate(popular_movies.iterrows()):
            display_movie_card(movie, cols[idx % 4])

if __name__ == "__main__":
    main()