"""
Interface Module

Provides different user interfaces for the recommender system
"""

from .cli import run_cli
from .streamlit_app import main as run_streamlit

__all__ = [
    'run_cli',
    'run_streamlit'
]