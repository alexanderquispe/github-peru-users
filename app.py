import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Peru GitHub Community Dashboard",
    page_icon="🇵🇪",
    layout="wide"
)

# Paths
PLOTS_DIR = "plots"

# Titles
st.title("🇵🇪 Peru GitHub Community Dashboard")
st.markdown("""
This dashboard presents an analysis of the GitHub developer community in Peru. 
The data was collected using the GitHub API, focusing on 100 users and a detailed sample of repositories from 10 random users.
""")

# Check for plots directory and images
if not os.path.exists(PLOTS_DIR):
    st.error(f"❌ '{PLOTS_DIR}' directory not found. Please run `visualize_github_data.py` first.")
else:
    # Create Tabs
    tab1, tab2 = st.tabs(["👤 User Level Stats", "📦 Repo Level Stats"])

    # Helper to display image with description
    def display_plot(filename, title, description):
        img_path = os.path.join(PLOTS_DIR, filename)
        if os.path.exists(img_path):
            st.header(title)
            st.image(img_path, use_container_width=True)
            st.info(description)
        else:
            st.warning(f"⚠️ Figure '{filename}' not found.")

    with tab1:
        st.subheader("Analysis of Peruvian GitHub Users")
        # User Influence
        display_plot(
            "top_followed_users.png",
            "1. Top 10 Most Followed Users",
            "This chart identifies the most influential GitHub users in our sample of 100 Peruvian developers. Followers are a key metric of influence within the platform."
        )

        st.divider()

        # Developer Activity
        display_plot(
            "repo_distribution.png",
            "2. Distribution of Public Repositories",
            "This histogram shows how many public repositories users typically maintain. It provides insight into the general activity level and project output of developers."
        )

    with tab2:
        st.subheader("Analysis of Repositories from Sampled Users")
        # Tech Stack
        display_plot(
            "language_distribution.png",
            "1. Most Common Programming Languages",
            "An analysis of the programming languages used in the repositories of the sampled developers. This shows the dominant technologies and skill sets in the Peru developer community."
        )

        st.divider()

        # Popular Projects
        display_plot(
            "top_starred_repos.png",
            "2. Top 10 Most Starred Repositories",
            "Highlighting the most popular projects (measured by stars) from our repository sample. These projects represent successful open-source contributions from Peru."
        )

        st.divider()

        # Correlations
        display_plot(
            "size_vs_stars.png",
            "3. Repository Size vs. Stars",
            "Investigating the relationship between the size of a repository (in KB) and its popularity (stars). This scatter plot helps identify if larger codebases attract more community attention."
        )

# Footer
st.markdown("---")
st.markdown("Data extracted via GitHub API | Analysis with Pandas & Seaborn | Powered by Streamlit")
