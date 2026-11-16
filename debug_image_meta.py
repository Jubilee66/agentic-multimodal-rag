# debug_image_meta.py

import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db_img"
)

collection = client.get_collection(
    "image_collection"
)

print(
    collection.peek()
)