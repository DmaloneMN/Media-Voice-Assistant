import os
from azure.cosmos import CosmosClient
import pandas as pd

def update_user_preferences():
    client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
    container = client.get_database_client("MediaDatabase").get_container_client("Users")
    
    # Example: Update preferences based on viewing history
    items = list(container.query_items(
        query="SELECT * FROM c WHERE c.last_watched IS NOT NULL",
        enable_cross_partition_query=True
    ))
    
    for user in items:
        # Example logic: Update preferred genre based on most watched
        if 'viewing_history' in user:
            genre_counts = {}
            for item in user['viewing_history']:
                for genre in item.get('genres', []):
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            if genre_counts:
                preferred_genre = max(genre_counts, key=genre_counts.get)
                container.patch_item(
                    item=user['id'],
                    partition_key=user['id'],
                    patch_operations=[
                        {"op": "add", "path": "/preferred_genre", "value": preferred_genre}
                    ]
                )
    
    print(f"Updated preferences for {len(items)} users")

if __name__ == "__main__":
    update_user_preferences()
