"""
Configuration Module

Provides access to settings and constants
"""

from .settings import (
    TMDB_API_KEY,
    MOVIES_DATA_PATH,
    CREDITS_DATA_PATH
)

__all__ = [
    'TMDB_API_KEY',
    'MOVIES_DATA_PATH',
    'CREDITS_DATA_PATH'
]