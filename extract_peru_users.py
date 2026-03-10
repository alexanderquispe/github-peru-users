"""
extract_peru_users.py
----------------------
Fetches up to 1000 GitHub users with location:Peru
and retrieves their full profile details.
Output: peru_users_1000.csv
"""

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ── Auth ──────────────────────────────────────────────────────────────────────
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"
else:
    print("⚠️  No GITHUB_TOKEN found – rate limits will be low (60 req/hr).")

OUTPUT_FILE = "peru_users_100.csv"
TARGET      = 100   # Fetch 100 users

# ── Step 1: Collect up to 1000 logins via Search API ─────────────────────────
print("=== Step 1: Searching for users with location:Peru ===")
logins = []
page   = 1

while len(logins) < TARGET:
    url = (
        f"https://api.github.com/search/users"
        f"?q=location:Peru&per_page=100&page={page}"
    )
    resp = requests.get(url, headers=HEADERS)

    # Handle Search rate limit (30 req/min for authenticated users)
    if resp.status_code == 403:
        reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset_ts - time.time(), 0) + 2
        print(f"  Rate limited (Search). Sleeping {wait:.0f}s …")
        time.sleep(wait)
        continue  # retry same page

    if resp.status_code != 200:
        print(f"  Search error {resp.status_code}: {resp.text}")
        break

    items = resp.json().get("items", [])
    if not items:
        print("  No more results.")
        break

    logins.extend([u["login"] for u in items])
    total_count = resp.json().get("total_count", "?")
    print(f"  Page {page}: got {len(items)} users  |  collected {len(logins)} / {TARGET}  |  API total_count = {total_count}")

    page += 1
    time.sleep(1)   # be polite to Search API

logins = list(dict.fromkeys(logins))[:TARGET]   # deduplicate, keep order
print(f"\n✅ Unique logins collected: {len(logins)}\n")

# ── Step 2: Fetch full profile for each login ─────────────────────────────────
print("=== Step 2: Fetching full user profiles ===")
records = []

for i, login in enumerate(logins, start=1):
    user_url = f"https://api.github.com/users/{login}"
    resp = requests.get(user_url, headers=HEADERS)

    # Handle Core rate limit (5000 req/hr for authenticated users)
    if resp.status_code == 403 or resp.status_code == 429:
        reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset_ts - time.time(), 0) + 2
        print(f"  [{i}] Rate limited. Sleeping {wait:.0f}s …")
        time.sleep(wait)
        resp = requests.get(user_url, headers=HEADERS)   # retry once

    if resp.status_code != 200:
        print(f"  [{i}] ✗ {login}  →  HTTP {resp.status_code}")
        continue

    records.append(resp.json())

    if i % 50 == 0 or i == len(logins):
        print(f"  Fetched {i}/{len(logins)} profiles …")

    time.sleep(0.3)   # ~3 req/s – well within 5000/hr limit

# ── Step 3: Save to CSV ───────────────────────────────────────────────────────
print(f"\n=== Step 3: Saving to {OUTPUT_FILE} ===")
df = pd.DataFrame(records)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n✅ Done!")
print(f"  Rows    : {len(df)}")
print(f"  Columns : {len(df.columns)}")
print(f"  File    : {os.path.abspath(OUTPUT_FILE)}")
print(f"\nColumns saved:\n  {list(df.columns)}")
