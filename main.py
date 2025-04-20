import argparse
from interface.cli import run_cli
from interface.streamlit_app import main as run_streamlit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie Recommendation System")
    parser.add_argument('--ui', choices=['cli', 'streamlit'], default='cli',
                       help='Choose the user interface (cli or streamlit)')
    
    args = parser.parse_args()
    
    if args.ui == 'cli':
        run_cli()
    else:
        run_streamlit()