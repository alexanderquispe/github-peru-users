import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def search_users(query, per_page=100):
    """
    Searches for users based on a query.
    Note: GitHub Search API is limited to 1000 results.
    """
    users = []
    page = 1
    
    while True:
        url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
        print(f"Fetching page {page} of search results...")
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error fetching search results: {response.status_code}")
            print(response.json())
            break
            
        data = response.json()
        items = data.get("items", [])
        users.extend(items)
        
        if len(items) < per_page or page * per_page >= 1000:
            break
            
        page += 1
        # Small delay to respect rate limits if not using a token
        if not GITHUB_TOKEN:
            time.sleep(2)
            
    return users

def get_user_details(username):
    """
    Fetches detailed profile information for a specific user.
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching details for {username}: {response.status_code}")
        return None
        
    return response.json()

def main():
    # 1. Search for users in Peru
    # We use location:Peru to find users.
    query = "location:Peru"
    print(f"Starting search for users with query: {query}")
    search_results = search_users(query)
    print(f"Found {len(search_results)} users in search results (max 1000).")

    # 2. Fetch full details for each user to see all available columns
    detailed_users = []
    # For initial testing, let's just fetch a few to see the structure
    # The user wants "all" data, but for the "analyze columns" part, 
    # we need to fetch a few full profiles.
    
    limit = 20 # Let's fetch 20 for initial column analysis
    print(f"Fetching detailed profiles for the first {limit} users to analyze data fields...")
    
    for i, user in enumerate(search_results[:limit]):
        username = user["login"]
        details = get_user_details(username)
        if details:
            detailed_users.append(details)
        
        # Periodically show progress
        if (i + 1) % 5 == 0:
            print(f"Processed {i + 1}/{limit} users...")

    # 3. Create DataFrame and export
    df = pd.DataFrame(detailed_users)
    
    # Analyze columns
    print("\n--- Available Columns (Data Fields) ---")
    print(df.columns.tolist())
    
    # Save to CSV
    output_file = "peru_users_preview.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved detailed data to {output_file}")
    
    # Find all unique users (based on login)
    unique_logins = [u["login"] for u in search_results]
    print(f"Total Unique Users Found in Search: {len(set(unique_logins))}")

if __name__ == "__main__":
    main()
