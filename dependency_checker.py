##Imports
from packaging.specifiers import SpecifierSet


def find_missing_dependencies(requirements, installed_packages):
    missing = []

    for package_name in requirements:
        if package_name not in installed_packages:
            missing.append(package_name)

    return missing


def find_version_mismatches(requirements, installed_packages):
    mismatches = []

    for package_name, required_version in requirements.items():
        if package_name not in installed_packages:
            continue

        if not required_version:
            continue

        specifier = SpecifierSet(required_version)
        installed_version = installed_packages[package_name]

        if installed_version not in specifier:
            mismatches.append({
                "package": package_name,
                "required": required_version,
                "installed": installed_version,
            })

    return mismatches