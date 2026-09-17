from package_checker import get_installed_packages


def test_installed_packages():
    packages = get_installed_packages()

    assert isinstance(packages, dict)
    assert "flask" in packages
    assert "pytest" in packages
    assert "packaging" in packages