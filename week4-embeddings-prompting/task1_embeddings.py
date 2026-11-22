import itertools
import os
import numpy as np
import requests
import llm_client

SENTENCES = [
    "The cat is sitting on the mat",
    "A kitten rests on the rug",
    "The stock market fell sharply today",
    "Shares dropped as investors panicked",
    "I forgot my password",
    "How do I reset my login credentials?",
    "The bank by the river was flooded",
    "I deposited money at the bank",
]


def embed_with_api(texts, model):
    base = llm_client.BASE_URL
    if base.endswith("/chat/completions"):
        base = base[: -len("/chat/completions")]
    headers = {"Authorization": f"Bearer {llm_client.API_KEY}", "Content-Type": "application/json"}
    r = requests.post(f"{base}/embeddings", headers=headers,
                      json={"model": model, "input": texts}, timeout=60)
    r.raise_for_status()
    return np.array([item["embedding"] for item in r.json()["data"]])


def embed_locally(texts):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2").encode(texts)


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


model = os.getenv("EMBEDDING_MODEL")
if model:
    print("Using API model:", model)
    embeddings = embed_with_api(SENTENCES, model)
else:
    print("Using local model: all-MiniLM-L6-v2")
    embeddings = embed_locally(SENTENCES)

print("Vector size:", embeddings.shape[1])
print()

pairs = []
for i, j in itertools.combinations(range(len(SENTENCES)), 2):
    pairs.append((cosine(embeddings[i], embeddings[j]), SENTENCES[i], SENTENCES[j]))

pairs.sort(reverse=True)
for score, a, b in pairs:
    print(f"{score:.3f} | {a}  <->  {b}")