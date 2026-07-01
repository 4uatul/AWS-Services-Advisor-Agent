from advisor import advisor

# Test queries to run
queries = [
    "I need a database that handles 10,000 reads per second with low latency"
]

for q in queries:
    print(f"\n--- Query: {q} ---")
    response = advisor(q)