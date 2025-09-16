"""
Silver transformation layer: Chunk media data for RAG, add metadata, prepare for embedding.
Handles TMDb JSON and SQL user preferences.
"""
import os
from dotenv import load_dotenv
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sqlite3
from typing import List

load_dotenv()

def load_media_data(file_path: str) -> List:
    """Load TMDb JSON data."""
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".[] | {text: .overview, metadata: {title: .title, genre: .genres[0].name if .genres else 'unknown'}}"
    )
    return loader.load()

def load_user_prefs(db_path: str) -> List:
    """Load user preferences from SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, favorite_genres FROM preferences")
    docs = [{"text": row[1], "metadata": {"user_id": row[0], "type": "user_pref"}} for row in cursor.fetchall()]
    conn.close()
    return docs

def chunk_data(docs: List, chunk_size: int = 300, overlap: int = 50) -> List:
    """Chunk data using RecursiveCharacterTextSplitter for RAG."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". "]  # Preserve media plot sentences
    )
    return splitter.split_documents(docs)

if __name__ == "__main__":
    # Example usage
    movie_docs = load_media_data("gold/movies.json")
    user_docs = load_user_prefs("gold/user_prefs.db")
    all_docs = movie_docs + user_docs
    chunks = chunk_data(all_docs)
    print(f"Generated {len(chunks)} chunks. Example: {chunks[0]}")
    # Save chunks to file for next step (e.g., embedding)
    # with open("gold/chunks.json", "w") as f:
    #     json.dump([{"text": c.page_content, "metadata": c.metadata} for c in chunks], f)
