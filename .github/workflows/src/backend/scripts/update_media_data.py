import os
from azure.cosmos import CosmosClient
import pandas as pd
import requests

# Initialize Cosmos DB client
client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
database = client.get_database_client("MediaDatabase")
container = database.get_container_client("MediaCatalog")

def fetch_latest_movies():
    """Fetch latest movies from TMDB API"""
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/now_playing?api_key={os.getenv('TMDB_API_KEY')}"
    )
    return response.json()["results"]

def update_cosmos_db():
    movies = fetch_latest_movies()
    
    for movie in movies:
        # Transform data to match your schema
        document = {
            'id': str(movie['id']),
            'title': movie['title'],
            'genre': movie['genre_ids'],  # This would need mapping to genre names
            'rating': movie['vote_average'],
            'release_date': movie['release_date'],
            'type': 'movie',
            'partitionKey': 'movie'  # Example partition key
        }
        
        # Upsert document
        container.upsert_item(body=document)
    
    print(f"Updated {len(movies)} movies in Cosmos DB")

if __name__ == "__main__":
    update_cosmos_db()
