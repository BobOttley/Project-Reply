# === config.py ===

import os
import json
import pickle
from dotenv import load_dotenv
from openai import OpenAI

# --- Load environment variables ---
load_dotenv()

# --- OpenAI client ---
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY)

# --- Model Names and Thresholds ---
EMBED_MODEL               = "text-embedding-3-small"
SIMILARITY_THRESHOLD      = 0.30
RESPONSE_LIMIT            = 3
STANDARD_MATCH_THRESHOLD  = 0.85

# --- Extraction Config Folder ---
EXTRACTION_CONFIG_FOLDER = "config"

# --- Load School Knowledge Base (local only for now) ---
def load_kb():
    with open("embeddings/metadata.pkl", "rb") as f:
        kb = pickle.load(f)
        doc_embeddings = kb["embeddings"]
        metadata = kb["metadata"]
    return doc_embeddings, metadata

# --- Load Standard Replies (local only for now) ---
def load_standard_responses(embed_fn):
    path = "standard_responses.json"
    messages, embeddings, replies = [], [], []
    if not os.path.exists(path):
        print("⚠️ No standard_responses.json found.")
        return messages, embeddings, replies
    try:
        with open(path, "r") as f:
            saved = json.load(f)
        for entry in saved:
            msg = entry["message"]
            rep = entry["reply"]
            messages.append(msg)
            embeddings.append(embed_fn(msg))
            replies.append(rep)
        print(f"✅ Loaded {len(messages)} template replies.")
    except Exception as e:
        print(f"❌ Failed loading templates: {e}")
    return messages, embeddings, replies

# --- Load Extraction Config Utility ---
from utils.config_loader import load_extraction_config
