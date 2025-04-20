import requests
from config.settings import TMDB_API_KEY

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    @staticmethod
    def get_movie_poster_url(poster_path):
        """Get full poster URL from poster path"""
        return f"{TMDBService.IMAGE_BASE_URL}{poster_path}" if poster_path else None

    @staticmethod
    def get_movie_details(movie_id):
        """Get additional movie details from TMDb API"""
        url = f"{TMDBService.BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None