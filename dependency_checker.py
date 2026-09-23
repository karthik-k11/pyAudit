def find_missing_dependencies(requirements, installed_packages):
    missing = []

    for package_name in requirements:
        if package_name not in installed_packages:
            missing.append(package_name)

    return missing