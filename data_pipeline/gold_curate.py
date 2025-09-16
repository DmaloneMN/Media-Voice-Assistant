"""
Gold curation: Prepare curated datasets for RAG KBs with metadata.
"""
import json
from typing import List

def curate_chunks(chunks: List, output_file: str):
    """Curate and save chunks with enhanced metadata for RAG."""
    curated = [{"text": chunk.page_content, "metadata": {**chunk.metadata, "processed": True}} for chunk in chunks]
    with open(output_file, "w") as f:
        json.dump(curated, f, indent=2)
    print(f"Curated {len(curated)} chunks to {output_file}")

if __name__ == "__main__":
    # Assume chunks from silver_transform
    from silver_transform import chunk_data  # Import if in same dir
    docs = []  # Load from previous
    chunks = chunk_data(docs)
    curate_chunks(chunks, "gold/curated_media.json")
