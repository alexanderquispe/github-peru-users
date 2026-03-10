import os
import time
import random
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

OUTPUT_FILE = "peru_repos_10users.csv"
SEARCH_TARGET = 100  # Initial pool to sample from
SAMPLE_SIZE = 10     # Number of users to sample
random.seed(42)      # For reproducibility

# ── Step 1: Load logins from existing CSV ──────────────────────────────────────
INPUT_CSV = "peru_users_100.csv"
print(f"=== Step 1: Loading logins from {INPUT_CSV} ===")
if not os.path.exists(INPUT_CSV):
    print(f"❌ Error: {INPUT_CSV} not found. Please run extract_peru_users.py first.")
    exit(1)

df_users = pd.read_csv(INPUT_CSV)
if 'login' not in df_users.columns:
    print(f"❌ Error: 'login' column not found in {INPUT_CSV}.")
    exit(1)

logins = df_users['login'].tolist()
print(f"  Loaded {len(logins)} logins.")

# ── Step 2: Randomly sample 10 users ──────────────────────────────────────────
print(f"\n=== Step 2: Sampling {SAMPLE_SIZE} random users ===")
sampled_logins = random.sample(logins, min(len(logins), SAMPLE_SIZE))
print(f"  Sampled users: {', '.join(sampled_logins)}")

# ── Step 3: Fetch all repositories for each sampled user ───────────────────────
print("\n=== Step 3: Fetching all repositories for sampled users ===")
all_repos = []

for idx, login in enumerate(sampled_logins, start=1):
    print(f"  [{idx}/{SAMPLE_SIZE}] Fetching repos for: {login}...")
    user_repos = []
    repo_page = 1
    
    while True:
        repos_url = f"https://api.github.com/users/{login}/repos?per_page=100&page={repo_page}"
        resp = requests.get(repos_url, headers=HEADERS)

        if resp.status_code in [403, 429]:
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset_ts - time.time(), 0) + 2
            print(f"    Rate limited. Sleeping {wait:.0f}s …")
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            print(f"    Error fetching repos for {login}: {resp.status_code}")
            break

        page_data = resp.json()
        if not page_data:
            break

        user_repos.extend(page_data)
        if len(page_data) < 100:
            break
        
        repo_page += 1
        time.sleep(0.5)

    # Add owner_login for easy linkage
    for repo in user_repos:
        repo['owner_login'] = login
        all_repos.append(repo)
    
    print(f"    Added {len(user_repos)} repositories.")
    time.sleep(0.5)

# ── Step 4: Save to CSV ───────────────────────────────────────────────────────
print(f"\n=== Step 4: Saving {len(all_repos)} repos to {OUTPUT_FILE} ===")
if all_repos:
    df = pd.DataFrame(all_repos)
    
    # Flatten 'owner' and 'license' objects if they exist
    if 'owner' in df.columns:
        owner_df = pd.json_normalize(df['owner']).add_prefix('owner_')
        df = pd.concat([df.drop(columns=['owner']), owner_df], axis=1)
        
    if 'license' in df.columns:
        # Some values might be None
        license_data = [x if x is not None else {} for x in df['license']]
        license_df = pd.json_normalize(license_data).add_prefix('license_')
        df = pd.concat([df.drop(columns=['license']), license_df], axis=1)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ Done! Saved to {os.path.abspath(OUTPUT_FILE)}")
    print(f"Columns: {list(df.columns)}")
else:
    print("❌ No repositories found.")
