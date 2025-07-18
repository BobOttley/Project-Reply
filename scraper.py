# === scraper.py ===

import os
import requests
import re
import pickle
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

# === CONFIG ===
START_URL = "https://www.morehouse.org.uk/"    # CHANGE ME!
DOMAIN = "morehouse.org.uk"                    # CHANGE ME!
EMBED_MODEL = "text-embedding-3-small"
MAX_DEPTH = 2                             # Limit crawl depth for safety

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_KEY, "No OpenAI API key found!"
client = OpenAI(api_key=OPENAI_KEY)

visited = set()
chunks = []
metadata = []

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    [s.extract() for s in soup(["script", "style", "header", "footer", "nav"])]
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def chunk_text(text, max_tokens=350):
    paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 40]
    chunks = []
    chunk = ""
    for p in paras:
        if len((chunk + " " + p).split()) < max_tokens:
            chunk += " " + p
        else:
            if chunk.strip():
                chunks.append(chunk.strip())
            chunk = p
    if chunk.strip():
        chunks.append(chunk.strip())
    return chunks

def crawl(url, depth=0):
    if depth > MAX_DEPTH or url in visited or DOMAIN not in urlparse(url).netloc:
        return
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return
        html = resp.text
        text = clean_text(html)
        for chunk in chunk_text(text):
            chunks.append(chunk)
            metadata.append({
                "url": url,
                "text": chunk
            })
        visited.add(url)
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if link.startswith("mailto:") or link.startswith("tel:"):
                continue
            crawl(link, depth+1)
    except Exception as e:
        print(f"❌ Error at {url}: {e}")

def embed_chunks(chunks):
    vectors = []
    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}…")
        resp = client.embeddings.create(model=EMBED_MODEL, input=[chunk])
        vectors.append(resp.data[0].embedding)
    return vectors

if __name__ == "__main__":
    print(f"🌐 Crawling {START_URL}…")
    crawl(START_URL)
    print(f"✅ Crawled {len(chunks)} chunks.")

    with open("chunks.jsonl", "w") as f:
        for i, chunk in enumerate(chunks):
            json.dump({"id": i, "text": chunk}, f)
            f.write("\n")
    print("✅ chunks.jsonl written.")

    print("🧠 Embedding chunks…")
    embeddings = embed_chunks(chunks)
    print("✅ Embeddings complete.")

    # Save metadata.pkl
    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump({"embeddings": embeddings, "metadata": metadata}, f)
    print("✅ embeddings/metadata.pkl written.")
