from tools.vector_search_tool import search_documents

print("=" * 80)
print("TESTING VECTOR DATABASE")
print("=" * 80)

query = "What is Artificial Intelligence?"

results = search_documents(
    query=query,
    n_results=3
)

print(results)

print("\n")
print("=" * 80)
print("TEST COMPLETED")
print("=" * 80)