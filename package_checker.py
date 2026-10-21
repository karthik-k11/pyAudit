import json
import subprocess
import sys

_PACKAGE_PROBE = """
import importlib.metadata
import importlib.util
import json
import re
import sys

def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()

requested = {normalize(name) for name in json.loads(sys.argv[1])}
installed = {}
for distribution in importlib.metadata.distributions():
    name = distribution.metadata.get("Name")
    if name:
        installed[normalize(name)] = distribution.version

modules_by_distribution = {}
for module, distribution_names in importlib.metadata.packages_distributions().items():
    for distribution_name in distribution_names:
        normalized_name = normalize(distribution_name)
        if normalized_name in requested:
            modules_by_distribution.setdefault(normalized_name, []).append(module)

imports = {}
for name in requested:
    candidates = modules_by_distribution.get(name) or [name.replace("-", "_")]
    available = False
    for candidate in candidates:
        try:
            if importlib.util.find_spec(candidate.split(".", 1)[0]) is not None:
                available = True
                break
        except (ImportError, ValueError):
            continue
    imports[name] = available

print(json.dumps({"installed": installed, "imports": imports}))
"""


def inspect_python_packages(python_executable=None, package_names=()):
    executable = str(python_executable or sys.executable)
    try:
        result = subprocess.run(
            [
                executable,
                "-c",
                _PACKAGE_PROBE,
                json.dumps(list(package_names)),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(
            f"Could not inspect installed packages using {executable}: {exc}"
        ) from exc

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Python interpreter at {executable} returned invalid package data."
        ) from exc


def get_installed_packages(python_executable=None):
    return inspect_python_packages(python_executable)["installed"]


def check_imports(package_names, python_executable=None):
    return inspect_python_packages(python_executable, package_names)["imports"]