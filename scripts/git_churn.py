"""Git churn via pydriller when installed; falls back to git log parsing."""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def via_pydriller(max_commits: int = 200) -> dict[str, object]:
    from pydriller import Repository

    churn: dict[str, dict[str, int]] = defaultdict(lambda: {"commits": 0, "added": 0, "removed": 0})
    commits_seen = 0
    for commit in Repository(str(ROOT)).traverse_commits():
        commits_seen += 1
        for modified in commit.modified_files:
            path = modified.new_path or modified.old_path
            if not path:
                continue
            churn[path]["commits"] += 1
            churn[path]["added"] += modified.added_lines or 0
            churn[path]["removed"] += modified.deleted_lines or 0
        if commits_seen >= max_commits:
            break
    return _payload(commits_seen, churn)


def via_git() -> dict[str, object]:
    churn: dict[str, dict[str, int]] = defaultdict(lambda: {"commits": 0, "added": 0, "removed": 0})
    log = subprocess.run(
        ["git", "log", "--numstat", "--pretty=format:COMMIT"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    commits_seen = 0
    for line in log.stdout.splitlines():
        if line == "COMMIT":
            commits_seen += 1
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, path = parts
        if added == "-" or removed == "-":
            continue
        churn[path]["commits"] += 1
        churn[path]["added"] += int(added)
        churn[path]["removed"] += int(removed)
    return _payload(commits_seen, churn)


def _payload(commits_seen: int, churn: dict[str, dict[str, int]]) -> dict[str, object]:
    top = sorted(churn.items(), key=lambda item: item[1]["commits"], reverse=True)[:15]
    return {
        "commits_analyzed": commits_seen,
        "files_touched": len(churn),
        "top_churned_files": [{"path": path, **stats} for path, stats in top],
    }


def main() -> None:
    try:
        payload = via_pydriller()
        payload["engine"] = "pydriller"
    except Exception:
        payload = via_git()
        payload["engine"] = "git"
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
