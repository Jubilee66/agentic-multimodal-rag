#=========================================================
# Image
#  ↓
# CLIP
#  ↓
# Embedding
# (Phase1-Phase5)
#=========================================================
# =========================================================
# Step 4: Extract Images + Page Context
# =========================================================
# =========================================================
# Step 4: Extract Useful Images Only
# =========================================================

from pathlib import Path
import json
import io

import pymupdf
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

IMAGE_DIR = DATA_DIR / "extracted_images"

MANIFEST_FILE = BASE_DIR / "image_manifest.json"


def extract_images(clean_output=False):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if clean_output:

        for old_file in IMAGE_DIR.iterdir():

            if old_file.is_file():
                old_file.unlink()

    manifest = []

    total_images = 0

    skipped_images = 0

    for pdf_path in sorted(
        DATA_DIR.glob("*.pdf")
    ):

        print(
            f"\nProcessing: {pdf_path.name}"
        )

        try:

            with pymupdf.open(pdf_path) as pdf:

                pdf_image_count = 0

                for page_index, page in enumerate(pdf):

                    page_text = page.get_text(
                        "text"
                    )

                    seen_xrefs = set()

                    for image_index, image_info in enumerate(
                        page.get_images(
                            full=True
                        )
                    ):

                        xref = image_info[0]

                        if xref in seen_xrefs:
                            continue

                        seen_xrefs.add(xref)

                        try:

                            extracted = pdf.extract_image(
                                xref
                            )

                            image_bytes = extracted.get(
                                "image"
                            )

                            extension = extracted.get(
                                "ext",
                                "png"
                            )

                            if not image_bytes:
                                continue

                            img = Image.open(
                                io.BytesIO(
                                    image_bytes
                                )
                            )

                            width, height = img.size

                            # =================================
                            # FILTER 1:
                            # Remove tiny images
                            # =================================

                            if width < 300:
                                skipped_images += 1
                                continue

                            if height < 300:
                                skipped_images += 1
                                continue

                            # =================================
                            # FILTER 2:
                            # Remove banner-like logos
                            # =================================

                            ratio = width / height

                            if ratio > 4:
                                skipped_images += 1
                                continue

                            if ratio < 0.25:
                                skipped_images += 1
                                continue

                            # =================================
                            # SAVE IMAGE
                            # =================================

                            image_name = (
                                f"{pdf_path.stem}"
                                f"_page_{page_index + 1}"
                                f"_img_{image_index + 1}"
                                f".{extension}"
                            )

                            output_path = (
                                IMAGE_DIR / image_name
                            )

                            output_path.write_bytes(
                                image_bytes
                            )

                            manifest.append({

                                "image":
                                    image_name,

                                "file_path":
                                    str(
                                        output_path.resolve()
                                    ),

                                "source_pdf":
                                    str(
                                        pdf_path.relative_to(
                                            BASE_DIR
                                        )
                                    ),

                                "page_number":
                                    page_index + 1,

                                "xref":
                                    int(xref),

                                "width":
                                    width,

                                "height":
                                    height,

                                "page_text":
                                    page_text[:10000]
                            })

                            pdf_image_count += 1
                            total_images += 1

                        except Exception as ex:

                            print(
                                f"Image skipped: {ex}"
                            )

                print(
                    f"Saved {pdf_image_count} images"
                )

        except Exception as exc:

            print(
                f"ERROR processing "
                f"{pdf_path.name}: {exc}"
            )

    MANIFEST_FILE.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\n" + "=" * 50)

    print(
        f"Useful images saved: "
        f"{total_images}"
    )

    print(
        f"Images filtered out: "
        f"{skipped_images}"
    )

    print(
        f"Manifest saved: "
        f"{MANIFEST_FILE}"
    )

    print("=" * 50)

    return manifest


if __name__ == "__main__":

    extract_images(
        clean_output=True
    )

# import pymupdf
# import os

# # =====================================
# # FOLDERS
# # =====================================

# DATA_FOLDER = "data"

# IMAGE_OUTPUT_FOLDER = os.path.join(
#     DATA_FOLDER,
#     "extracted_images"
# )

# os.makedirs(
#     IMAGE_OUTPUT_FOLDER,
#     exist_ok=True
# )

# # =====================================
# # PROCESS ALL PDFs
# # =====================================

# total_images = 0

# for file_name in os.listdir(DATA_FOLDER):

#     if not file_name.lower().endswith(".pdf"):
#         continue

#     pdf_path = os.path.join(
#         DATA_FOLDER,
#         file_name
#     )

#     print(f"\nProcessing: {file_name}")

#     try:

#         doc = pymupdf.open(pdf_path)

#         image_count = 0

#         for page_num in range(len(doc)):

#             page = doc.load_page(page_num)

#             image_list = page.get_images(
#                 full=True
#             )

#             for image_index, img in enumerate(
#                 image_list
#             ):

#                 xref = img[0]

#                 base_image = doc.extract_image(
#                     xref
#                 )

#                 image_bytes = base_image[
#                     "image"
#                 ]

#                 image_ext = base_image[
#                     "ext"
#                 ]

#                 image_name = (
#                     f"{os.path.splitext(file_name)[0]}"
#                     f"_page_{page_num + 1}"
#                     f"_img_{image_index}"
#                     f".{image_ext}"
#                 )

#                 image_path = os.path.join(
#                     IMAGE_OUTPUT_FOLDER,
#                     image_name
#                 )

#                 with open(
#                     image_path,
#                     "wb"
#                 ) as image_file:

#                     image_file.write(
#                         image_bytes
#                     )

#                 image_count += 1
#                 total_images += 1

#         print(
#             f"Extracted {image_count} images"
#         )

#     except Exception as e:

#         print(
#             f"Error processing "
#             f"{file_name}: {e}"
#         )

# print("\n===================================")
# print(f"TOTAL IMAGES: {total_images}")
# print("Image extraction complete.")
# print("===================================")