import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

url = "https://api.github.com/search/users?q=location:Peru"
response = requests.get(url, headers=HEADERS)
data = response.json()
total_count = data.get("total_count", 0)

with open("total_count.txt", "w") as f:
    f.write(str(total_count))

print(f"Total count written to total_count.txt: {total_count}")
