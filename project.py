import requests
import logging
import os
from dotenv import load_dotenv
import smtplib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename="workflow_monitor.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Workflow status
GITHUB_API_URL = "https://api.github.com"
REPO_GITHUB = os.getenv("REPO_GITHUB")  # Format: "owner/repo"
TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")  # Your GitHub Access Token

# Email notification
EMAIL_HOST = os.getenv("EMAIL_HOST")  # Email Provider Host URL
EMAIL_PORT = os.getenv("EMAIL_PORT")  # Email Provider Connection Port
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")  # Your Email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Your Email Password
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Your sending email
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Your receiving email

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
    if status in ["failure", "timed_out", "action_required"]:
        logging.info(f"Latest Workflow Status: {status} - Sending failure notification email...")
        send_failure_notification(status)
        logging.info(f"Notification email sent")
    elif status:
        logging.info(f"Latest Workflow Status: {status}")
    else:
        logging.warning("Failed to fetch workflow status")

def send_failure_notification(status):
    try:
        smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        message = f"""\
Subject: Github workflow failed
To: {EMAIL_RECEIVER}
From: {EMAIL_SENDER}

Last workflow status: {status}."""
        print(f"[*] Sending message: {message}")
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
        print(f"[*] Message sent")

        smtp.quit()

    except:
        logging.error(f"Failed to send email to notify of workflow status. Message: {message}.")
        smtp.quit()

def main():
    status = fetch_workflow_status()
    log_status(status)

if __name__ == "__main__":
    main()
