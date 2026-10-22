from environment_checker import get_environment_info
from environment_checker import resolve_python_interpreter


def test_environment_info():
    info = get_environment_info()

    assert "python_version" in info
    assert "python_executable" in info
    assert "operating_system" in info
    assert "virtual_environment" in info
    assert "virtual_environment_path" in info


def test_project_virtual_environment_is_selected(tmp_path):
    interpreter = tmp_path / ".venv" / "Scripts" / "python.exe"
    interpreter.parent.mkdir(parents=True)
    interpreter.touch()

    selected, source = resolve_python_interpreter(tmp_path)

    assert selected == interpreter
    assert source == "Project virtual environment"