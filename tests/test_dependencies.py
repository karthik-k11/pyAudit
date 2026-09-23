from dependency_checker import find_missing_dependencies


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