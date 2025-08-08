import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment
URL = os.getenv("COSMOS_URL")  # Format: "https://YOUR_ACCOUNT.documents.azure.com:443/"
KEY = os.getenv("COSMOS_KEY")  # Primary or secondary key

if not URL or not KEY:
    raise ValueError("Missing Cosmos DB credentials in environment variables")

# Initialize client with proper credential format
client = CosmosClient(URL, credential=KEY)

# Database and container setup
database = client.create_database_if_not_exists(id="MediaDatabase")

# Users container
database.create_container_if_not_exists(
    id="Users",
    partition_key="/id",
    unique_key_policy={'uniqueKeys': [{'paths': ['/email']}]}
)

# Media container
database.create_container_if_not_exists(
    id="MediaCatalog",
    partition_key="/genre",
    indexing_policy={
        'indexingMode': 'consistent',
        'includedPaths': [{'path': '/*'}]
    }
)

print("Database and containers initialized successfully!")
