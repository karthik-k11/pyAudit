from package_checker import get_installed_packages
from package_checker import check_imports


def test_installed_packages():
    packages = get_installed_packages()

    assert isinstance(packages, dict)
    assert "flask" in packages
    assert "pytest" in packages
    assert "packaging" in packages


def test_import_checks_use_distribution_metadata():
    checks = check_imports(
        ["Flask", "pyaudit-package-that-does-not-exist"]
    )

    assert checks == {
        "flask": True,
        "pyaudit-package-that-does-not-exist": False,
    }