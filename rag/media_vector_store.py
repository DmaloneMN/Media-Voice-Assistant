from langchain.embeddings import AzureOpenAIEmbeddings  # Azure integration
from langchain.vectorstores import FAISS  # Or Azure Cosmos DB vector search

# Azure embeddings (use your Azure OpenAI endpoint)
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://your-azure-openai-instance.openai.azure.com/",
    api_key="your-azure-key",
    model="text-embedding-ada-002"
)

# From previous chunks
movie_kb = FAISS.from_documents(chunks, embeddings)  # Movie-specific KB
tv_kb = FAISS.from_documents(tv_chunks, embeddings)   # TV KB

# Retrieve example
query = "Recommend sci-fi movies like Inception"
relevant_docs = movie_kb.similarity_search(query, k=3)
print([doc.metadata["title"] for doc in relevant_docs])  # e.g., ['Interstellar', 'Blade Runner']
