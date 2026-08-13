from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "quality" / "reports"
SRC = ROOT / "src"


def run(command: list[str], report_name: str) -> dict[str, object]:
    target = REPORTS / report_name
    target.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    target.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    return {
        "tool": report_name,
        "exit_code": completed.returncode,
        "command": command,
        "report": str(target.relative_to(ROOT)),
    }


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    results = [
        run([python, "-m", "pytest", "tests", "--cov=orderflow", "--cov-branch", "--cov-report=xml:quality/reports/coverage/coverage.xml", "--cov-report=term-missing"], "coverage/pytest.txt"),
        run([python, "-m", "flake8", "src"], "flake8/flake8.txt"),
        run([python, "-m", "pylint", "src/orderflow", "--exit-zero"], "pylint/pylint.txt"),
        run([python, "-m", "bandit", "-r", "src/orderflow", "-f", "json", "-o", str(REPORTS / "bandit" / "bandit.json")], "bandit/bandit-run.txt"),
        run([python, "-m", "radon", "cc", "src", "-s", "-j"], "radon/radon.json"),
        run([python, "-m", "pip_audit", "-r", "requirements.txt", "-f", "json"], "pip-audit/pip-audit.json"),
        run([python, str(ROOT / "scripts" / "git_churn.py")], "git_churn/git_churn.json"),
    ]
    summary = REPORTS / "summary.json"
    summary.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
