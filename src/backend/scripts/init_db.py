from azure.cosmos import CosmosClient
import os

URL = os.getenv("COSMOS_URL")  # Get from: terraform output -raw cosmosdb_endpoint
KEY = os.getenv("COSMOS_KEY")  # Get from: az cosmosdb keys list --name [NAME] --resource-group [RG]

client = CosmosClient(URL, credential=KEY)
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
