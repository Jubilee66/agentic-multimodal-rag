from pathlib import Path

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

BASE_DIR = Path(__file__).resolve().parents[1]

DB_DIR = BASE_DIR / "chroma_db_txt"

MODEL_NAME = "all-MiniLM-L6-v2"

COLLECTION_NAME = "rag_docs"

model = SentenceTransformer(
    MODEL_NAME
)

client = chromadb.PersistentClient(
    path=str(DB_DIR)
)

collection = client.get_collection(
    COLLECTION_NAME
)


def search_documents(
    query: str,
    n_results: int = 5
):

    embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )[0].tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    output = []

    docs = results["documents"][0]

    metas = results["metadatas"][0]

    distances = results["distances"][0]

    for doc, meta, dist in zip(
        docs,
        metas,
        distances
    ):

        output.append({

            "content":
                doc,

            "source":
                meta.get(
                    "source",
                    "Unknown"
                ),

            "type":
                meta.get(
                    "type",
                    ""
                ),

            "distance":
                float(dist)
        })

    return output



# import chromadb
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )

# client = chromadb.PersistentClient(
#     path="./chroma_db_txt"
# )

# collection = client.get_collection(
#     "rag_docs"
# )

# def search_documents(
#     query: str,
#     n_results: int = 5
# ):

#     embedding = model.encode(
#         query
#     ).tolist()

#     results = collection.query(
#         query_embeddings=[embedding],
#         n_results=n_results
#     )

#     docs = results["documents"][0]
#     metas = results["metadatas"][0]

#     output = []

#     for doc, meta in zip(
#         docs,
#         metas
#     ):
#         output.append(
#             f"""
# SOURCE:
# {meta["source"]}

# CONTENT:
# {doc}
# """
#         )

#     return "\n\n".join(output)
