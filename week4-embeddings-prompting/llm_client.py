
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
API_KEY = os.getenv("API_KEY", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5.6-luna")


def chat(prompt):

    if not BASE_URL or not API_KEY:
        raise ValueError("BASE_URL or API_KEY is missing.")

    url = (
        BASE_URL
        if BASE_URL.endswith("/chat/completions")
        else f"{BASE_URL}/chat/completions"
    )

    body = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=60
        )

        r.raise_for_status()

        data = r.json()

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except requests.exceptions.ConnectionError:
        print("Connection failed.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"Invalid API response: {e}")

    return None
