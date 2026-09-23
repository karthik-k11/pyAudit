from dependency_checker import find_missing_dependencies, find_version_mismatches, find_undeclared_packages


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