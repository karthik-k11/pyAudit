from environment_checker import get_environment_info


def test_environment_info():
    info = get_environment_info()

    assert "python_version" in info
    assert "python_executable" in info
    assert "operating_system" in info
    assert "virtual_environment" in info
    assert "virtual_environment_path" in info