from project import fetch_workflow_status

def test_fetch_workflow_status():
    status = fetch_workflow_status()
    assert status == "No recent workflows found"