from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate

llm = AzureOpenAI(
    azure_endpoint="https://your-azure-openai-instance.openai.azure.com/",
    api_key="your-azure-key",
    model="gpt-4o"
)

# Router (semantic, using descriptions)
route_descriptions = [
    {"name": "movie", "description": "Queries about movies, films, cinema recommendations."},
    {"name": "tv", "description": "Queries about TV shows, series, episodes."}
]
route_index = FAISS.from_texts([r["description"] for r in route_descriptions], embeddings)

def route_media_query(query):
    docs = route_index.similarity_search(query, k=1)
    return route_descriptions[0 if "movie" in docs[0].page_content.lower() else 1]["name"]  # Simplified

# Agent tools
kb_map = {"movie": movie_kb.as_retriever(), "tv": tv_kb.as_retriever()}
tools = [
    Tool(name="Movie Recommender", func=lambda q: RetrievalQA.from_chain_type(llm, retriever=kb_map["movie"]).run(q), description="For movie queries"),
    Tool(name="TV Recommender", func=lambda q: RetrievalQA.from_chain_type(llm, retriever=kb_map["tv"]).run(q), description="For TV queries")
]
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# Run example
query = "Recommend a sci-fi TV show"
dept = route_media_query(query)
response = agent.run(f"{query} (Route to {dept})")
print(response)  # e.g., "Based on retrieved data: Watch 'The Expanse' – a space thriller."
