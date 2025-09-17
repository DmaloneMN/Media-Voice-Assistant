```python
"""
Bronze ingestion layer: Fetch raw media data from TMDb API and create sample user preferences in SQLite.
Outputs to gold/movies.json, gold/tv_shows.json, gold/user_prefs.db for RAG pipeline.
"""

import os
import requests
import json
import sqlite3
from dotenv import load_dotenv
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_tmdb_data(endpoint: str, pages: int = 1) -> List[Dict]:
    """
    Fetch data from TMDb API (movies or TV shows).
    Args:
        endpoint: API endpoint (e.g., 'movie/popular', 'tv/popular')
        pages: Number of pages to fetch (default: 1, ~20 items per page)
    Returns:
        List of items with title, overview, genres.
    """
    results = []
    for page in range(1, pages + 1):
        url = f"{TMDB_BASE_URL}/{endpoint}?api_key={TMDB_API_KEY}&page={page}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            results.extend(data.get("results", []))
            logger.info(f"Fetched page {page} from {endpoint}: {len(data['results'])} items")
        except requests.RequestException as e:
            logger.error(f"Error fetching {endpoint}, page {page}: {e}")
            continue
    return results

def clean_tmdb_data(items: List[Dict], item_type: str) -> List[Dict]:
    """
    Clean TMDb data, ensuring required fields and adding metadata.
    Args:
        items: Raw TMDb data
        item_type: 'movie' or 'tv'
    Returns:
        Cleaned items with title, overview, genres, and metadata.
    """
    cleaned = []
    for item in items:
        title = item.get("title" if item_type == "movie" else "name", "Unknown")
        overview = item.get("overview", "")
        genres = [g["name"] for g in item.get("genres", [])] or ["unknown"]
        if overview:  # Only include items with valid overview for RAG
            cleaned.append({
                "text": overview,
                "metadata": {
                    "title": title,
                    "genres": genres,
                    "type": item_type
                }
            })
    logger.info(f"Cleaned {len(cleaned)} {item_type} items")
    return cleaned

def save_to_json(data: List[Dict], file_path: str):
    """Save data to JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(data)} items to {file_path}")
    except IOError as e:
        logger.error(f"Error saving to {file_path}: {e}")

def create_user_prefs_db(db_path: str):
    """Create sample user preferences SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                favorite_genres TEXT
            )
        """)
        # Sample data for testing
        sample_prefs = [
            (1, "sci-fi, thriller"),
            (2, "comedy, drama"),
            (3, "action, adventure")
        ]
        cursor.executemany("INSERT OR REPLACE INTO preferences (user_id, favorite_genres) VALUES (?, ?)", sample_prefs)
        conn.commit()
        logger.info(f"Created user preferences database at {db_path} with {len(sample_prefs)} entries")
    except sqlite3.Error as e:
        logger.error(f"Error creating database {db_path}: {e}")
    finally:
        conn.close()

def main():
    """Main function to fetch and save TMDb and user data."""
    # Create gold directory if not exists
    os.makedirs("gold", exist_ok=True)

    # Fetch movies and TV shows
    movies = fetch_tmdb_data("movie/popular", pages=2)  # ~40 movies
    tv_shows = fetch_tmdb_data("tv/popular", pages=2)   # ~40 TV shows

    # Clean data
    cleaned_movies = clean_tmdb_data(movies, "movie")
    cleaned_tv = clean_tmdb_data(tv_shows, "tv")

    # Save to gold layer
    save_to_json(cleaned_movies, "gold/movies.json")
    save_to_json(cleaned_tv, "gold/tv_shows.json")

    # Create user preferences database
    create_user_prefs_db("gold/user_prefs.db")

if __name__ == "__main__":
    if not TMDB_API_KEY:
        logger.error("TMDB_API_KEY not set in .env")
    else:
        main()
```
