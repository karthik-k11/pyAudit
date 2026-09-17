from requirements_parser import parse_requirements


def test_parse_requirements(tmp_path):
    requirements_file = tmp_path / "requirements.txt"

    requirements_file.write_text(
        "Flask==3.1.3\n"
        "pytest==9.1.1\n"
        "packaging==26.3\n",
        encoding="utf-8"
    )

    requirements = parse_requirements(requirements_file)

    assert requirements["flask"] == "==3.1.3"
    assert requirements["pytest"] == "==9.1.1"
    assert requirements["packaging"] == "==26.3"