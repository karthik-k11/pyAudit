import sqlite3
from pathlib import Path
from datetime import datetime


DATABASE_PATH = Path(__file__).resolve().parent / "database" / "pyaudit.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            audit_time TEXT NOT NULL,
            python_version TEXT NOT NULL,
            total_dependencies INTEGER NOT NULL,
            missing_dependencies INTEGER NOT NULL,
            version_mismatches INTEGER NOT NULL,
            undeclared_packages INTEGER NOT NULL,
            health_score INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_audit(project_name, audit_result):
    environment = audit_result["environment"]
    health = audit_result["health"]

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO audits (
            project_name,
            audit_time,
            python_version,
            total_dependencies,
            missing_dependencies,
            version_mismatches,
            undeclared_packages,
            health_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            project_name,
            datetime.now().isoformat(timespec="seconds"),
            environment["python_version"],
            audit_result["total_dependencies"],
            len(audit_result["missing_dependencies"]),
            len(audit_result["version_mismatches"]),
            len(audit_result["undeclared_packages"]),
            health["score"],
        ),
    )

    connection.commit()
    connection.close()


def get_audit_history():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            project_name,
            audit_time,
            python_version,
            total_dependencies,
            missing_dependencies,
            version_mismatches,
            undeclared_packages,
            health_score
        FROM audits
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return rows