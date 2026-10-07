from database import init_db, save_audit, get_audit_history


def test_save_and_get_audit(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.DATABASE_PATH",
        database_path,
    )

    init_db()

    audit_result = {
        "environment": {
            "python_version": "3.12.8",
        },
        "total_dependencies": 3,
        "missing_dependencies": [],
        "version_mismatches": [],
        "undeclared_packages": ["colorama"],
        "health": {
            "score": 85,
        },
    }

    save_audit("TestProject", audit_result)

    history = get_audit_history()

    assert len(history) == 1
    assert history[0][1] == "TestProject"
    assert history[0][3] == "3.12.8"
    assert history[0][4] == 3
    assert history[0][5] == 0
    assert history[0][6] == 0
    assert history[0][7] == 1
    assert history[0][8] == 85