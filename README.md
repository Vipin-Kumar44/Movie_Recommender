# 🎬 Movie Recommendation System (Developed with Python 3.9)

A content-based recommendation engine that suggests similar movies using TF-IDF and cosine similarity.

## Features
- Content-based filtering using movie metadata (genres, overview, cast, crew)
- Fuzzy title matching for misspelled queries
- Rating filters and customizable result count
- TMDb API integration for movie posters
- Streamlit web interface

## Installation

   1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie-recommender.git
   cd movie-recommender
## Install dependencies:
   pip install -r requirements.txt
## Project Structure
   movie-recommender/
   ├── data/                   # Movie datasets
   ├── config/                 # Configuration files
   ├── services/               # Core recommendation logic
   ├── utils/                  # Data processing utilities
   ├── interface/              # User interfaces
   ├── tests/                  # Unit tests
   ├── requirements.txt        # Dependencies
   └── README.md               # This file

## Customization
   Adjust min_rating in the interface for quality filters
   Modify n parameter in recommend() for more/less results
   Add new features to content_features in data_loader.py

## Troubleshooting
   "Movie not found" → Try different spellings
    No posters showing → Check TMDb API key
    Slow performance → Reduce dataset size during development

## Future Improvements
   Add user ratings system
   Implement hybrid recommendation
   Add watchlist feature
   Include trending movies section
