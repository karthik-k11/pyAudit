from importlib.metadata import distributions


def get_installed_packages():
    packages = {}

    for package in distributions():
        name = package.metadata["Name"]
        version = package.version

        if name:
            packages[name.lower()] = version

    return packages