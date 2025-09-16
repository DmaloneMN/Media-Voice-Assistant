"""
Utils for generating embeddings using Azure OpenAI.
"""
from langchain.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embeddings():
    """Initialize Azure OpenAI embeddings."""
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        model="text-embedding-ada-002"
    )

def embed_chunks(chunks, embeddings):
    """Embed list of chunks."""
    # For full integration, use in vector_store/build_index.py
    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
    return vectors

if __name__ == "__main__":
    embeddings = get_embeddings()
    test_text = ["Test movie synopsis for embedding."]
    print(embeddings.embed_query(test_text[0]))  # Outputs vector
