from packaging.requirements import Requirement


def parse_requirements(file_path):
    requirements = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            requirement = Requirement(line)

            requirements[requirement.name.lower()] = str(requirement.specifier)

    return requirements