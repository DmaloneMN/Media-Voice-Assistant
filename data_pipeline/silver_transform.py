from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sqlite3

# Load TMDb JSON
loader = JSONLoader(file_path="gold/movies.json", jq_schema=".[] | {text: .overview, metadata: {title: .title, genre: .genres}}")
docs = loader.load()

# Load user preferences from SQL
conn = sqlite3.connect("gold/user_prefs.db")
cursor = conn.cursor()
cursor.execute("SELECT user_id, favorite_genres FROM preferences")
user_docs = [{"text": row[1], "metadata": {"user_id": row[0]}} for row in cursor.fetchall()]
conn.close()

# Chunk data
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
movie_chunks = splitter.split_documents(docs)
user_chunks = splitter.split_documents(user_docs)

# Output: [{"text": "Inception is a sci-fi thriller...", "metadata": {"title": "Inception", "genre": "sci-fi"}}, ...]
print(movie_chunks[0])
