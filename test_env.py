import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

print("ENV PATH =", BASE_DIR / ".env")
print("KEY =", os.getenv("GROQ_API_KEY"))