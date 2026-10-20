import json
import subprocess
import sys
from pathlib import Path


_ENVIRONMENT_PROBE = """
import json
import platform
import sys

print(json.dumps({
    "python_version": platform.python_version(),
    "python_executable": sys.executable,
    "operating_system": platform.system(),
    "virtual_environment": sys.prefix != sys.base_prefix,
    "virtual_environment_path": sys.prefix if sys.prefix != sys.base_prefix else None,
    "python_full_version": platform.python_version(),
    "sys_platform": sys.platform,
    "platform_system": platform.system(),
    "platform_machine": platform.machine(),
    "implementation_name": sys.implementation.name,
    "implementation_version": platform.python_version(),
}))
"""


def resolve_python_interpreter(project_directory=None):
    """Prefer a project's conventional virtual environment when one exists."""
    if project_directory is not None:
        project_directory = Path(project_directory)
        candidates = (
            project_directory / ".venv" / "Scripts" / "python.exe",
            project_directory / ".venv" / "bin" / "python",
            project_directory / "venv" / "Scripts" / "python.exe",
            project_directory / "venv" / "bin" / "python",
        )
        for candidate in candidates:
            if candidate.is_file():
                return candidate, "Project virtual environment"

    return Path(sys.executable), "PyAudit's current environment (fallback)"


def get_environment_info(python_executable=None, interpreter_source=None):
    executable = str(python_executable or sys.executable)
    try:
        result = subprocess.run(
            [executable, "-c", _ENVIRONMENT_PROBE],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(
            f"Could not inspect Python interpreter at {executable}: {exc}"
        ) from exc

    try:
        environment = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Python interpreter at {executable} returned invalid environment data."
        ) from exc

    environment["interpreter_source"] = (
        interpreter_source or "Selected Python interpreter"
    )
    return environment