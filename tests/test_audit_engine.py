from audit_engine import run_audit


def test_run_audit():
    result = run_audit("requirements.txt")

    assert "environment" in result
    assert "total_dependencies" in result
    assert "missing_dependencies" in result
    assert "version_mismatches" in result
    assert "undeclared_packages" in result
    assert "health" in result

    assert result["total_dependencies"] == 3
    assert result["missing_dependencies"] == []
    assert result["version_mismatches"] == []