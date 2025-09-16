data_pipeline/utils/chunking.py
"""
Dedicated chunking utilities for media data in RAG pipeline.
Supports fixed-length, content-aware, and semantic chunking.
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from typing import List

class MediaChunker:
    def __init__(self, strategy: str = "fixed"):
        self.strategy = strategy
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    def fixed_chunk(self, docs: List) -> List:
        """Fixed-length chunking for media synopses."""
        return self.splitter.split_documents(docs)

    def content_aware_chunk(self, docs: List) -> List:
        """Chunk by media fields (e.g., overview, cast)."""
        # Assume docs have metadata; split per field
        chunks = []
        for doc in docs:
            if "overview" in doc.metadata:
                chunks.append({"text": doc.page_content, "metadata": doc.metadata})  # Simple split
        return self.splitter.split_documents(chunks)

    def semantic_chunk(self, sentences: List) -> List:
        """Semantic clustering for similar plots."""
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = embedder.encode(sentences)
        kmeans = KMeans(n_clusters=3)  # e.g., 3 semantic groups
        clusters = kmeans.fit_predict(embeddings)
        chunks = [[sentences[i] for i in range(len(sentences)) if clusters[i] == c] for c in set(clusters)]
        return chunks

if __name__ == "__main__":
    # Example
    chunker = MediaChunker("fixed")
    sample_docs = [{"page_content": "Inception is a sci-fi thriller about dreams."}]
    chunks = chunker.fixed_chunk(sample_docs)
    print(chunks)
