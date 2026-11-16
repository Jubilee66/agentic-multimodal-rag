from pathlib import Path
import json
import hashlib
import numpy as np
import chromadb

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "chroma_db_img"

EMBEDDINGS_FILE = BASE_DIR / "image_embeddings.npy"

CAPTION_FILE = BASE_DIR / "image_captions.json"

MANIFEST_FILE = BASE_DIR / "image_manifest.json"

COLLECTION_NAME = "image_collection"


def load_json(path):

    if not path.exists():
        return []

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def build_image_vector_store(
    reset=True
):

    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(
            "Run step5_generate_image_embeddings.py first."
        )

    records = np.load(
        EMBEDDINGS_FILE,
        allow_pickle=True
    )

    captions = load_json(
        CAPTION_FILE
    )

    manifest = load_json(
        MANIFEST_FILE
    )

    caption_map = {
        item["image"]: item["caption"]
        for item in captions
    }

    manifest_map = {
        item["image"]: item
        for item in manifest
    }

    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    if reset:
        try:
            client.delete_collection(
                COLLECTION_NAME
            )
        except:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    for item in records:

        image_name = str(item["image"])

        caption = caption_map.get(
            image_name,
            "No caption available"
        )

        manifest_item = manifest_map.get(
            image_name,
            {}
        )

        file_path = str(
            manifest_item.get(
                "file_path",
                ""
            )
        )

        image_id = hashlib.sha1(
            image_name.encode()
        ).hexdigest()

        collection.upsert(
            ids=[image_id],
            embeddings=[
                np.asarray(
                    item["embedding"],
                    dtype=np.float32
                ).tolist()
            ],
            metadatas=[{
                "image": image_name,
                "file_path": file_path,
                "caption": caption,
                "source_pdf":
                    manifest_item.get(
                        "source_pdf",
                        ""
                    ),
                "page_number":
                    manifest_item.get(
                        "page_number",
                        0
                    ),
                "page_text":
                    manifest_item.get(
                        "page_text",
                        ""
                    )[:10000]
            }]
        )

        print(
            f"Indexed: {image_name}"
        )

    print(
        f"\nTotal images indexed: "
        f"{collection.count()}"
    )


if __name__ == "__main__":
    build_image_vector_store(
        reset=True
    )




# import chromadb
# import numpy as np
# import json

# client = chromadb.PersistentClient(
#     path="./chroma_db_img"
# )

# collection = client.get_or_create_collection(
#     name="image_collection"
# )

# data = np.load(
#     "image_embeddings.npy",
#     allow_pickle=True
# )

# with open(
#     "image_captions.json",
#     "r",
#     encoding="utf-8"
# ) as f:

#     captions = json.load(f)

# caption_lookup = {
#     item["image"]: item["caption"]
#     for item in captions
# }

# for idx, item in enumerate(data):

#     image_name = item["image"]

#     caption = caption_lookup.get(
#         image_name,
#         "No caption available"
#     )

#     collection.add(
#         ids=[
#             f"img_{idx}"
#         ],
#         embeddings=[
#             item["embedding"].tolist()
#         ],
#         metadatas=[
#             {
#                 "image": image_name,
#                 "caption": caption,
#                 "path": f"extracted_images/{image_name}" # image path 
#             }
#         ]
#     )

#     print(
#         f"Stored: {image_name}"
#     )

# print(
#     "\nImage collection updated successfully."
# )

# import chromadb
# import numpy as np

# client = chromadb.PersistentClient(
#     path="./chroma_db"
# )

# collection = client.get_or_create_collection(
#     "image_collection"
# )

# data = np.load(
#     "image_embeddings.npy",
#     allow_pickle=True
# )

# for idx, item in enumerate(data):

#     collection.add(
#         ids=[str(idx)],
#         embeddings=[item["embedding"].tolist()],
#         metadatas=[
#             {
#                 "image": item["image"]
#             }
#         ]
#     )

# print("Images stored")