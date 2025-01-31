import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_API_URL = "https://api.github.com"
REPO_GITHUB = os.getenv("REPO_GITHUB")  # Format: "owner/repo"
TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")  # GitHub Personal Access Token 

def fetch_workflow_status():
    """Fetch the latest workflow run status from GitHub Actions API."""
    url = f"{GITHUB_API_URL}/repos/{REPO_GITHUB}/actions/runs"
    headers = {"Authorization": f"token {TOKEN_GITHUB}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "workflow_runs" in data and len(data["workflow_runs"]) > 0:
            return data["workflow_runs"][0]["status"]
        return "No recent workflows found"
    
    except requests.RequestException as e:
        logging.error(f"Error fetching workflow status: {e}")
        return None

def main():
    status = fetch_workflow_status()
    print(status)

if __name__ == "__main__":
    main()
