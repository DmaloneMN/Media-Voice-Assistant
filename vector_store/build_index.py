from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS  # Or Azure Cosmos DB
from azure.cosmos import CosmosClient

# Azure OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://your-azure-openai-instance.openai.azure.com/",
    api_key="your-azure-key",
    model="text-embedding-ada-002"
)

# Build movie and TV KBs
movie_kb = FAISS.from_documents(movie_chunks, embeddings)
tv_kb = FAISS.from_documents(tv_chunks, embeddings)

# Optional: Azure Cosmos DB for production
cosmos_client = CosmosClient("your-cosmos-endpoint", "your-cosmos-key")
# Configure Cosmos DB vector search (requires setup in Azure portal)

# Save FAISS indices
movie_kb.save_local("vector_store/movie_index")
tv_kb.save_local("vector_store/tv_index")
