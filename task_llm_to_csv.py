import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load settings from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Stop early if a setting is missing
if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY or BASE_URL not found. Check your .env file.")

URL = BASE_URL
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Different inputs to send to the LLM
questions = ["What is Python?", "What is a REST API?", "What is JSON?"]
results = []

for q in questions:
    payload = {
        "model": "gpt-5.6-luna",
        "messages": [{"role": "user", "content": q}],
    }
    answer = ""
    try:
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
        r.raise_for_status()  # raise an error for 4xx/5xx status codes
        answer = r.json()["choices"][0]["message"]["content"]
        status = "ok"
    except requests.exceptions.Timeout:
        status = "error: timeout"
    except requests.exceptions.ConnectionError:
        status = "error: connection failed"
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        if code == 401:
            status = "error: invalid API key"
        elif code == 429:
            status = "error: too many requests"
        else:
            status = f"error: HTTP {code}"
    except requests.exceptions.RequestException as e:
        status = f"error: {e}"
    except (KeyError, IndexError, ValueError):
        status = "error: unexpected response format"

    results.append({"question": q, "answer": answer, "status": status})

# Save the results as CSV
df = pd.DataFrame(results)
df.to_csv("results.csv", index=False, encoding="utf-8-sig")
print(df)
