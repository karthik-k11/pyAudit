from requirements_parser import parse_requirements


def test_parse_requirements(tmp_path):
    requirements_file = tmp_path / "requirements.txt"

    requirements_file.write_text(
        "Flask==3.1.3\n"
        "pytest==9.1.1\n"
        "packaging==26.3\n",
        encoding="utf-8"
    )

    requirements, invalid_requirements = parse_requirements(
        requirements_file
    )

    assert requirements["flask"] == "==3.1.3"
    assert requirements["pytest"] == "==9.1.1"
    assert requirements["packaging"] == "==26.3"
    assert invalid_requirements == []


def test_invalid_requirement(tmp_path):
    requirements_file = tmp_path / "requirements.txt"

    requirements_file.write_text(
        "Flask==3.1.3\n"
        "this is not a valid requirement\n",
        encoding="utf-8"
    )

    requirements, invalid_requirements = parse_requirements(
        requirements_file
    )

    assert requirements["flask"] == "==3.1.3"
    assert len(invalid_requirements) == 1
    assert invalid_requirements[0]["line"] == 2


def test_requirement_markers_use_selected_environment(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "new-package>=1; python_version >= '3.13'\n"
        "old-package>=1; python_version < '3.13'\n",
        encoding="utf-8",
    )

    requirements, invalid_requirements = parse_requirements(
        requirements_file,
        {"python_version": "3.12"},
    )

    assert requirements == {"old-package": ">=1"}
    assert invalid_requirements == []