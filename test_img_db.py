import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db_img"
)

collection = client.get_collection(
    "image_collection"
)

print("Total Images:",
      collection.count())

results = collection.query(
    query_texts=[
        "transformer architecture"
    ],
    n_results=3
)

print(results)
