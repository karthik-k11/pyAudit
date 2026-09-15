import os
import platform
import sys


def get_environment_info():
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "operating_system": platform.system(),
        "virtual_environment": "VIRTUAL_ENV" in os.environ,
        "virtual_environment_path": os.environ.get("VIRTUAL_ENV"),
    }