from project import fetch_workflow_status

def test_fetch_workflow_status(mocker):
    mock_response = mocker.Mock()

    # Success fetching status
    mock_response.json.return_value = {
        "workflow_runs": [{"status": "success"}]
    }
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch("requests.get", return_value=mock_response)
    status = fetch_workflow_status()
    assert status == "success"