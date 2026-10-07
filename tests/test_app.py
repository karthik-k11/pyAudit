from app import app


def test_dashboard_loads():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"PyAudit" in response.data


def test_history_loads():
    client = app.test_client()

    response = client.get("/history")

    assert response.status_code == 200
    assert b"Audit History" in response.data


def test_invalid_project_path():
    client = app.test_client()

    response = client.post(
        "/",
        data={"project_path": "C:\\Invalid\\Project\\Path"},
    )

    assert response.status_code == 200
    assert b"Project path does not exist." in response.data