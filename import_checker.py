from importlib.util import find_spec


def check_import(package_name):
    return find_spec(package_name) is not None