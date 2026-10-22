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


def test_audit_uses_project_requirements(tmp_path, monkeypatch):
    (tmp_path / "requirements.txt").write_text(
        "pyaudit-package-that-is-not-installed>=1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.save_audit", lambda project_name, result: None)
    client = app.test_client()

    response = client.post(
        "/",
        data={"project_path": str(tmp_path)},
    )

    assert response.status_code == 200
    assert b"Missing dependency: pyaudit-package-that-is-not-installed" in response.data
    assert b"Audit Interpreter" in response.data