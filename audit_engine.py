from dependency_checker import (
    find_missing_dependencies,
    find_undeclared_packages,
    find_version_mismatches,
)
from environment_checker import get_environment_info, resolve_python_interpreter
from health_score import calculate_health_score
from package_checker import inspect_python_packages
from requirements_parser import parse_requirements


def run_audit(requirements_file, project_directory=None):
    python_executable, interpreter_source = resolve_python_interpreter(
        project_directory
    )
    environment = get_environment_info(python_executable, interpreter_source)

    requirements, invalid_requirements = parse_requirements(
        requirements_file,
        environment,
    )
    package_data = inspect_python_packages(
        python_executable,
        requirements,
    )
    installed_packages = package_data["installed"]

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

    import_checks = package_data["imports"]

    import_failures = [
        package_name
        for package_name, available in import_checks.items()
        if not available
    ]

    health = calculate_health_score(
        missing_count=len(missing),
        mismatch_count=len(mismatches),
        import_failure_count=len(import_failures),
        invalid_requirement_count=len(invalid_requirements),
    )

    return {
        "environment": environment,
        "interpreter_source": interpreter_source,
        "total_dependencies": len(requirements),
        "missing_dependencies": missing,
        "version_mismatches": mismatches,
        "undeclared_packages": undeclared,
        "import_checks": import_checks,
        "import_failures": import_failures,
        "invalid_requirements": invalid_requirements,
        "health": health,
    }