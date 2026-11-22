import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
API_KEY = os.getenv("API_KEY", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5.6-luna")


def chat(prompt):
    # If BASE_URL already ends with /chat/completions use it as is, else add it
    url = BASE_URL if BASE_URL.endswith("/chat/completions") else f"{BASE_URL}/chat/completions"
    body = {"model": CHAT_MODEL, "messages": [{"role": "user", "content": prompt}]}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]