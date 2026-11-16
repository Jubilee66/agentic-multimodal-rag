from pathlib import Path

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

BASE_DIR = Path(__file__).resolve().parents[1]

DB_DIR = BASE_DIR / "chroma_db_img"

COLLECTION_NAME = "image_collection"

MODEL_NAME = "clip-ViT-B-32"

_model = None


def get_model():

    global _model

    if _model is None:
        _model = SentenceTransformer(
            MODEL_NAME
        )

    return _model


def search_images(
    query,
    n_results=25,
    max_distance=1.2
):

    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    try:

        collection = client.get_collection(
            COLLECTION_NAME
        )

    except Exception:

        return []

    model = get_model()

    vector = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )[0].tolist()

    results = collection.query(
        query_embeddings=[vector],
        n_results=n_results,
        include=[
            "metadatas",
            "distances"
        ]
    )

    output = []

    for meta, distance in zip(
        results["metadatas"][0],
        results["distances"][0]
    ):

        if distance > max_distance:
            continue

        output.append({

            "image":
                meta.get("image", ""),

            "path":
                meta.get("file_path", ""),

            "caption":
                meta.get("caption", ""),

            "page_text":
                meta.get("page_text", ""),

            "source_pdf":
                meta.get("source_pdf", ""),

            "page_number":
                meta.get("page_number", 0),

            "distance":
                float(distance)
        })

    # ==================================
    # RERANK RESULTS
    # ==================================

    query_words = [
        w.lower()
        for w in query.split()
        if len(w.strip()) > 2
    ]

    query_phrase = query.lower()

    for item in output:

        score = 0

        image_name = item.get(
            "image",
            ""
        ).lower()

        caption = item.get(
            "caption",
            ""
        ).lower()

        page_text = item.get(
            "page_text",
            ""
        ).lower()

        searchable = (
            image_name
            + " "
            + caption
            + " "
            + page_text
        )

        if query_phrase in searchable:
            score += 150

        for word in query_words:

            if word in image_name:
                score += 80

            if word in caption:
                score += 60

            if word in page_text:
                score += 50

        # reward smaller distance

        score += int(
            max(
                0,
                (1.2 - item["distance"])
            ) * 50
        )

        # logo suppression

        logo_terms = [
            "logo",
            "emblem",
            "banner",
            "icon",
            "academy",
            "skill india",
            "training institute"
        ]

        if any(
            term in searchable
            for term in logo_terms
        ):
            score -= 50

        item["score"] = score

    output.sort(
        key=lambda x: (
            x["score"],
            -x["distance"]
        ),
        reverse=True
    )

    return output[:5]

# import chromadb

# def search_images(query: str, n_results: int = 3, max_distance: float = 1.2):
#     """
#     Searches the image vector store and filters out low-relevance results 
#     based on a distance threshold.
#     """
#     client = chromadb.PersistentClient(path="./chroma_db_img")
    
#     try:
#         collection = client.get_collection(name="image_collection")
#     except Exception:
#         return []

#     results = collection.query(
#         query_texts=[query],
#         n_results=n_results
#     )

#     valid_images = []
    
#     if not results or not results['ids'][0]:
#         return []

#     for i in range(len(results['ids'][0])):
#         distance = results['distances'][0][i]
#         metadata = results['metadatas'][0][i]
        
#         # DEBUG: Print distance in your terminal to tune max_distance
#         print(f"Image: {metadata.get('file_path')} | Distance: {distance}")

#         # If the distance is greater than your threshold, skip it entirely
#         if distance > max_distance:
#             continue

#         valid_images.append({
#             "path": metadata.get("file_path"),
#             "caption": metadata.get("caption", "No caption available")
#         })

#     return valid_images









# import os
# import chromadb
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer(
#     "clip-ViT-B-32"
# )

# client = chromadb.PersistentClient(
#     path="./chroma_db_img"
# )

# collection = client.get_collection(
#     "image_collection"
# )

# def search_images(
#     query,
#     n_results=5
# ):

#     query_embedding = model.encode(
#         query
#     )

#     results = collection.query(
#         query_embeddings=[
#             query_embedding.tolist()
#         ],
#         n_results=n_results
#     )

#     images = []

#     for meta in results["metadatas"][0]:

#         images.append({
#             "image": meta.get("image"),
#             "caption": meta.get("caption"),
#             "path":  os.path.join("data",metadata["path"])
#         })

#     return images