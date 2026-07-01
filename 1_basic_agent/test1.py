from advisor import advisor

# Test queries to run
queries = [
    "I need a database that handles 10,000 reads per second with low latency",
    "I want to make a rag chatbot for 500 pages and i need recomendation on the vector store for like 1000 people"
]

for q in queries:
    print(f"\n--- Query: {q} ---")
    response = advisor(q)