from dependency_checker import find_missing_dependencies, find_version_mismatches, find_undeclared_packages
from health_score import calculate_health_score


def test_missing_dependencies():
    requirements = {
        "flask": "==3.1.3",
        "pandas": "==2.3.1",
    }

    installed_packages = {
        "flask": "3.1.3",
    }

    missing = find_missing_dependencies(
        requirements,
        installed_packages
    )

    assert missing == ["pandas"]

def test_undeclared_packages():
    requirements = {
        "flask": "==3.1.3",
        "pytest": "==9.1.1",
    }

    installed_packages = {
        "flask": "3.1.3",
        "pytest": "9.1.1",
        "colorama": "0.4.6",
    }

    undeclared = find_undeclared_packages(
        requirements,
        installed_packages
    )

    assert undeclared == ["colorama"]

from import_checker import check_import


def test_import_check():
    assert check_import("flask") is True
    assert check_import("package_that_does_not_exist") is False

def test_healthy_score():
    result = calculate_health_score()

    assert result["score"] == 100
    assert result["status"] == "Healthy"


def test_score_with_issues():
    result = calculate_health_score(
        missing_count=1,
        mismatch_count=1,
    )

    assert result["score"] == 65
    assert result["status"] == "Needs Attention"


def test_score_never_below_zero():
    result = calculate_health_score(
        missing_count=10,
        mismatch_count=10,
        import_failure_count=10,
        invalid_requirement_count=10,
    )

    assert result["score"] == 0
    assert result["status"] == "Unhealthy"