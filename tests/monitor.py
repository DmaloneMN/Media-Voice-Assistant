import time
from ragas import evaluate
from datasets import Dataset

start_time = time.time()
response = agent.run(query)
latency = time.time() - start_time

# Evaluate RAG
dataset = Dataset.from_dict({
    "question": [query],
    "context": [context],
    "answer": [response]
})
results = evaluate(dataset, metrics=["faithfulness", "answer_relevance"])
print(f"Latency: {latency}s, Faithfulness: {results['faithfulness']}")
