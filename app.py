from pathlib import Path

from flask import Flask, render_template, request

from audit_engine import run_audit
from database import get_audit_history, init_db, save_audit
from report_generator import generate_report


app = Flask(__name__)

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    audit_result = None
    report = None
    error = None

    if request.method == "POST":
        project_path = request.form.get("project_path", "").strip()

        if not project_path:
            error = "Please enter a project path."
        else:
            project_directory = Path(project_path)
            requirements_file = project_directory / "requirements.txt"

            if not project_directory.is_dir():
                error = "Project path does not exist."
            elif not requirements_file.is_file():
                error = "requirements.txt was not found in the project."
            else:
                try:
                    audit_result = run_audit(requirements_file)
                    report = generate_report(audit_result)

                    save_audit(
                        project_directory.name,
                        audit_result,
                    )
                except Exception as exc:
                    error = str(exc)

    return render_template(
        "index.html",
        audit_result=audit_result,
        report=report,
        error=error,
    )


@app.route("/history")
def history():
    audits = get_audit_history()

    return render_template(
        "history.html",
        audits=audits,
    )


if __name__ == "__main__":
    app.run(debug=True)