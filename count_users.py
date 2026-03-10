import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# --- Step 1: Get total_count from Search API ---
url = "https://api.github.com/search/users?q=location:Peru&per_page=1"
response = requests.get(url, headers=HEADERS)
data = response.json()
total_count = data.get("total_count", "ERROR")

# --- Step 2: Paginate and collect all unique logins (up to API limit of 1000) ---
users = []
page = 1
SEARCH_LIMIT = 1000

while True:
    search_url = f"https://api.github.com/search/users?q=location:Peru&per_page=100&page={page}"
    r = requests.get(search_url, headers=HEADERS)
    items = r.json().get("items", [])
    users.extend(items)
    if len(items) < 100 or len(users) >= SEARCH_LIMIT:
        break
    page += 1
    time.sleep(0.5)

unique_logins = list(set([u["login"] for u in users]))

# --- Write results to file ---
with open("result.txt", "w") as f:
    f.write(f"total_count_from_api: {total_count}\n")
    f.write(f"fetched_pages: {page}\n")
    f.write(f"unique_logins_fetched: {len(unique_logins)}\n")

print("Done.")
