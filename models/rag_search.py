from langchain.llms import AzureOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from azure.cognitiveservices.speech import SpeechRecognizer

# Initialize LLM
llm = AzureOpenAI(azure_endpoint="https://your-azure-openai-instance.openai.azure.com/", api_key="your-azure-key", model="gpt-4o")

# Load KBs
movie_kb = FAISS.load_local("vector_store/movie_index", embeddings)
tv_kb = FAISS.load_local("vector_store/tv_index", embeddings)
user_kb = FAISS.load_local("vector_store/user_index", embeddings)

# Semantic router
route_descriptions = [
    {"name": "movie", "description": "Queries about movies, films, cinema recommendations."},
    {"name": "tv", "description": "Queries about TV shows, series, episodes."},
    {"name": "user", "description": "Queries about user preferences, personalized recs."}
]
route_index = FAISS.from_texts([r["description"] for r in route_descriptions], embeddings)

def route_media_query(query):
    docs = route_index.similarity_search(query, k=1)
    return next(r["name"] for r in route_descriptions if r["description"] in docs[0].page_content)

# Voice input
def get_voice_query():
    recognizer = SpeechRecognizer(subscription="your-speech-key", region="westus")
    result = recognizer.recognize_once()
    return result.text if result.reason == ResultReason.RecognizedSpeech else "Error"

# Agent tools
kb_map = {"movie": movie_kb.as_retriever(), "tv": tv_kb.as_retriever(), "user": user_kb.as_retriever()}
tools = [
    Tool(name="Movie Recommender", func=lambda q: RetrievalQA.from_chain_type(llm, retriever=kb_map["movie"]).run(q), description="For movie queries"),
    Tool(name="TV Recommender", func=lambda q: RetrievalQA.from_chain_type(llm, retriever=kb_map["tv"]).run(q), description="For TV queries"),
    Tool(name="User Preferences", func=lambda q: RetrievalQA.from_chain_type(llm, retriever=kb_map["user"]).run(q), description="For user-specific recs")
]
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# Run
query = get_voice_query() or "Recommend a sci-fi movie"
response = agent.run(f"{query} (Route to {route_media_query(query)})")
print(response)  # e.g., "Try 'Interstellar' – a sci-fi epic."
