# CI/CD Workflow Monitor and Logger
CS50p Final Project
### Description:
Python script that integrates with GitHub Actions's API to monitor the status of running workflows. It can log the results, send notifications on failures, and even retry failed jobs based on a set of criteria.
### Main Functions:
- `get_workflow_status()` – Fetches current workflow status from GitHub Actions API.
- `log_status()` – Logs workflow status into a log file or database.
- `send_failure_notification()` – Sends an email or Slack notification when a job fails.
### Tests:
Mock API responses using pytest and test logging and notification functions.
