import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)

# Paths
USERS_CSV = "peru_users_100.csv"
REPOS_CSV = "peru_repos_10users.csv"
PLOTS_DIR = "plots"

# Create plots directory if it doesn't exist
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)
    print(f"Created directory: {PLOTS_DIR}")

def generate_visualizations():
    # ── Load Data ────────────────────────────────────────────────────────────
    print("Loading data...")
    try:
        df_users = pd.read_csv(USERS_CSV)
        df_repos = pd.read_csv(REPOS_CSV)
    except FileNotFoundError as e:
        print(f"❌ Error: {e.filename} not found. Please ensure both CSVs are present.")
        return

    # 1. Top 10 Most Followed Users
    print("Generating: Top 10 Most Followed Users...")
    top_followed = df_users.nlargest(10, 'followers')
    plt.figure()
    sns.barplot(data=top_followed, x='followers', y='login', hue='login', palette="viridis", legend=False)
    plt.title("Top 10 Most Followed GitHub Users in Peru (Sample)", fontsize=16)
    plt.xlabel("Followers", fontsize=12)
    plt.ylabel("Username", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "top_followed_users.png"))
    plt.close()

    # 2. Most Common Programming Languages
    print("Generating: Most Common Programming Languages...")
    # Drop rows without language
    lang_counts = df_repos['language'].value_counts()
    plt.figure()
    sns.barplot(x=lang_counts.index, y=lang_counts.values, hue=lang_counts.index, palette="magma", legend=False)
    plt.title("Distribution of Programming Languages (Sample Repos)", fontsize=16)
    plt.xticks(rotation=45)
    plt.xlabel("Language", fontsize=12)
    plt.ylabel("Number of Repositories", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "language_distribution.png"))
    plt.close()

    # 3. Top 10 Most Starred Repositories
    print("Generating: Top 10 Most Starred Repositories...")
    top_starred_repos = df_repos.nlargest(10, 'stargazers_count')
    plt.figure()
    # Using full_name to distinguish repos
    sns.barplot(data=top_starred_repos, x='stargazers_count', y='full_name', hue='full_name', palette="crest", legend=False)
    plt.title("Top 10 Most Starred Repositories (Sample)", fontsize=16)
    plt.xlabel("Stars", fontsize=12)
    plt.ylabel("Repository", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "top_starred_repos.png"))
    plt.close()

    # 4. Distribution of Public Repositories (Users)
    print("Generating: Distribution of Public Repositories...")
    plt.figure()
    sns.histplot(df_users['public_repos'], kde=True, color="skyblue")
    plt.title("Distribution of Public Repository Counts per User", fontsize=16)
    plt.xlabel("Number of Public Repos", fontsize=12)
    plt.ylabel("Count of Users", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "repo_distribution.png"))
    plt.close()

    # 5. Repository Size vs. Stars (Correlation)
    print("Generating: Repository Size vs. Stars...")
    plt.figure()
    sns.scatterplot(data=df_repos, x='size', y='stargazers_count', alpha=0.6, color="coral")
    plt.title("Repository Size vs. Stars (Correlation)", fontsize=16)
    plt.xlabel("Size (KB)", fontsize=12)
    plt.ylabel("Stargazers Count", fontsize=12)
    # Log scale if data is very skewed
    if df_repos['size'].max() > 10000:
        plt.xscale('log')
        plt.xlabel("Size (KB) - Log Scale", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "size_vs_stars.png"))
    plt.close()

    print(f"\n✅ All visualizations saved in '{PLOTS_DIR}/' folder!")

if __name__ == "__main__":
    generate_visualizations()
