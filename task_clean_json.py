import requests
import pandas as pd

# 1. Download the JSON data
try:
    r = requests.get("https://dummyjson.com/users", timeout=15)
    r.raise_for_status()
    users = r.json()["users"]  # the list of users is inside the "users" key


except requests.exceptions.Timeout:
    print("Error: the request timed out.")
    raise SystemExit(1)

except requests.exceptions.ConnectionError:
    print("Error: could not connect. Check your internet.")
    raise SystemExit(1)

except requests.exceptions.HTTPError as e:
    print(f"Error: server returned HTTP {e.response.status_code}.")
    raise SystemExit(1)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    raise SystemExit(1)

except (KeyError, ValueError):
    print("Error: unexpected JSON format.")
    raise SystemExit(1)




# 2. Convert the JSON to a table (flattens nested fields)
df = pd.json_normalize(users)

# 3. Keep only the columns we need and rename them
try:
    df = df[["id", "firstName", "lastName", "age", "email", "address.city", "company.name"]]
except KeyError as e:
    print(f"Error: missing column in the data: {e}")
    raise SystemExit(1)

df = df.rename(columns={"address.city": "city", "company.name": "company"})

# 4. Clean the data
df = df.drop_duplicates()                               # remove duplicate rows
df["firstName"] = df["firstName"].str.strip()           # remove extra spaces
df["email"] = df["email"].str.lower()                   # make emails lowercase
df["age"] = pd.to_numeric(df["age"], errors="coerce")   # convert age to number
df = df.dropna(subset=["email"])                        # drop rows without email
df["age"] = df["age"].fillna(df["age"].median())        # fill missing ages



# 5. Save the clean data as CSV and JSON
try:
    df.to_csv("clean.csv", index=False)
    df.to_json("clean.json", orient="records", indent=2)
except PermissionError:
    print("Error: close clean.csv / clean.json if they are open, then run again.")
    raise SystemExit(1)
except OSError as e:
    print(f"Error: could not save the files: {e}")
    raise SystemExit(1)

print(df.head())