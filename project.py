import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename="workflow_monitor.log", level=logging.INFO, format="%(asctime)s - %(message)s")

GITHUB_API_URL = "https://api.github.com"
REPO_GITHUB = os.getenv("REPO_GITHUB")  # Format: "owner/repo"
TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")  # GitHub Personal Access Token 

def fetch_workflow_status():
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

def log_status(status):
    if status == "No recent workflows found":
        logging.info(status)
    elif status:
        logging.info(f"Latest Workflow Status: {status}")
    else:
        logging.warning("Failed to fetch workflow status")

def main():
    status = fetch_workflow_status()
    log_status(status)

if __name__ == "__main__":
    main()
