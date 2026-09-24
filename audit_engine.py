from environment_checker import get_environment_info
from package_checker import get_installed_packages
from requirements_parser import parse_requirements
from dependency_checker import (
    find_missing_dependencies,
    find_version_mismatches,
    find_undeclared_packages,
)
from health_score import calculate_health_score


def run_audit(requirements_file):
    environment = get_environment_info()
    installed_packages = get_installed_packages()
    requirements = parse_requirements(requirements_file)

    missing = find_missing_dependencies(
        requirements,
        installed_packages,
    )

    mismatches = find_version_mismatches(
        requirements,
        installed_packages,
    )

    undeclared = find_undeclared_packages(
        requirements,
        installed_packages,
    )

    health = calculate_health_score(
        missing_count=len(missing),
        mismatch_count=len(mismatches),
    )

    return {
        "environment": environment,
        "total_dependencies": len(requirements),
        "missing_dependencies": missing,
        "version_mismatches": mismatches,
        "undeclared_packages": undeclared,
        "health": health,
    }