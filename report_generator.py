def generate_report(audit_result):
    environment = audit_result["environment"]
    missing = audit_result["missing_dependencies"]
    mismatches = audit_result["version_mismatches"]
    undeclared = audit_result["undeclared_packages"]
    import_checks = audit_result["import_checks"]
    invalid_requirements = audit_result["invalid_requirements"]
    health = audit_result["health"]

    lines = [
        "PYAUDIT REPORT",
        "────────────────────────────",
        "",
        "Environment",
        f"Python Version : {environment['python_version']}",
        f"Executable     : {environment['python_executable']}",
        f"Operating System: {environment['operating_system']}",
        f"Virtual Env    : {'Detected' if environment['virtual_environment'] else 'Not detected'}",
        f"Environment Path: {environment['virtual_environment_path']}",
        f"Interpreter Source: {environment['interpreter_source']}",
        "",
        "Dependencies",
        f"Total          : {audit_result['total_dependencies']}",
        "",
        "Missing Dependencies",
    ]

    if missing:
        for package in missing:
            lines.append(f"✗ {package}")
    else:
        lines.append("✓ None")

    lines.extend([
        "",
        "Version Mismatches",
    ])

    if mismatches:
        for mismatch in mismatches:
            lines.append(f"⚠ {mismatch['package']}")
            lines.append(f"  Required : {mismatch['required']}")
            lines.append(f"  Installed: {mismatch['installed']}")
    else:
        lines.append("✓ None")

    lines.extend([
        "",
        "Undeclared Packages",
    ])

    if undeclared:
        for package in undeclared:
            lines.append(f"⚠ {package}")
    else:
        lines.append("✓ None")

    lines.extend([
        "",
        "Import Checks",
    ])

    for package, available in import_checks.items():
        status = "✓ Import available" if available else "✗ Import failed"
        lines.append(f"{package}: {status}")

    lines.extend([
        "",
        "Invalid Requirements",
    ])

    if invalid_requirements:
        for item in invalid_requirements:
            lines.append(
                f"✗ Line {item['line']}: {item['value']}"
            )
    else:
        lines.append("✓ None")

    lines.extend([
        "",
        "Health Score",
        f"{health['score']} / 100",
        health["status"],
        "",
        "Issues Summary",
        f"Missing dependencies : {len(missing)}",
        f"Version mismatches   : {len(mismatches)}",
        f"Import failures      : {len(audit_result['import_failures'])}",
        f"Invalid requirements : {len(invalid_requirements)}",
        f"Undeclared packages  : {len(undeclared)}",
    ])

    return "\n".join(lines)