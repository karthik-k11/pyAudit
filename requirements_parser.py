from packaging.requirements import InvalidRequirement, Requirement


def parse_requirements(file_path):
    requirements = {}
    invalid_requirements = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                requirement = Requirement(line)
                requirements[requirement.name.lower()] = str(
                    requirement.specifier
                )
            except InvalidRequirement:
                invalid_requirements.append({
                    "line": line_number,
                    "value": line,
                })

    return requirements, invalid_requirements