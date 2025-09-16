from langchain.document_loaders import JSONLoader  # For TMDb JSON
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load sample media data (e.g., from TMDb API or local JSON)
loader = JSONLoader(file_path="media_data/movies.json", jq_schema=".[] | {text: .overview, metadata: {title: .title, genre: .genres}}")
docs = loader.load()

# Chunk by content-aware (e.g., plot + metadata)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # Short for voice responses
    chunk_overlap=50,
    separators=["\n\n", "\n", ". "]  # Preserve sentences
)
chunks = splitter.split_documents(docs)

# Output: Chunks like {"text": "Inception is a sci-fi thriller...", "metadata": {"title": "Inception", "genre": "sci-fi"}}
print(chunks[0])
