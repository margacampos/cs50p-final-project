from project import fetch_workflow_status

def test_fetch_workflow_status(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock()

    # Should return fetched status
    mock_response.json.return_value = {
        "workflow_runs": [{"status": "success"}]
    }
    mocker.patch("requests.get", return_value=mock_response)
    status = fetch_workflow_status()
    assert status == "success"

    # Should return only the last workflow
    mock_response.json.return_value = {
        "workflow_runs": [{"status": "failure"}, {"status": "timed_out"}]
    }
    mocker.patch("requests.get", return_value=mock_response)
    status = fetch_workflow_status()
    assert status == "failure"

    # Should return "No recent workflows found" when there are no workflows
    mock_response.json.return_value = {
        "workflow_runs": []
    }
    mocker.patch("requests.get", return_value=mock_response)
    status = fetch_workflow_status()
    assert status == "No recent workflows found"