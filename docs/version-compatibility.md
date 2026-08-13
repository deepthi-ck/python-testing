# Version compatibility

Source: `Testable_Language_Version_Matrix_Verbatim_Fixed.xlsx` → sheet **Tool Matrix by Language** → Python columns (Tool, Supported Version).

## Runtime this repository targets

| Constraint | Value |
|---|---|
| `requires-python` | `>=3.10,<3.14` |
| CI matrix | 3.10, 3.11, 3.12 |
| Classifiers | 3.10, 3.11, 3.12, 3.13 |
| Syntax | 3.10-compatible (`list[str]`, `X \| None`, no 3.12 type aliases, no 3.11 except-groups) |

Python 3.10 is the overlap of Coverage.py, Pymcdc, pylint, Semgrep/Bandit, pip-audit, cosmic-ray, and testmon in the matrix. The application therefore analyses cleanly on every currently shipping CPython that Testable lists as first-class.

## Tool × versions from the matrix (verbatim)

| Tool | Supported versions listed in the matrix |
|---|---|
| Crosshair | 3.8, 3.9, 3.11, 3.13, 3.15 |
| Coverage.py | 3.10, 3.11, 3.12, 3.13, 3.16 |
| Pymcdc | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Radon/Lizard | 3.8, 3.9, 3.10, 3.11 |
| testmon | 3.10, 3.11, 3.12, 3.13, 3.14 |
| cognitive-ast | 3.8, 3.9, 3.10, 3.11, 3.12 |
| jscpd | 2.6, 2.7, 3.4, 3.5, 3.6 (language-agnostic scanner; still runs on this 3.10+ tree) |
| pylint | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Semgrep OSS + Bandit | 3.10, 3.11, 3.12, 3.13, 3.14 |
| pip-audit | 3.10, 3.11, 3.12, 3.13, 3.14 |
| cosmic-ray | 3.9, 3.10, 3.11, 3.12, 3.13 |

## Practical notes

- **3.14–3.16** appear in the matrix as forward-looking rows (Django main / future CPython). They are documented, not executed in CI, because those interpreters are not generally available.
- **Python 2.6/2.7** appear only on jscpd (a Node scanner). This repository does not ship Python 2 code.
- Optional analysis extras (crosshair-tool, pymcdc, complexipy, cosmic-ray, pytest-testmon, pydriller) are **not** runtime dependencies. Install them in the Testable execution environment when that tool is configured.

## Feature usage vs version

| Feature | Used? | Minimum Python |
|---|---|---|
| `from __future__ import annotations` | yes | 3.7+ |
| `list[str]` / `int \| None` | yes | 3.10 |
| `match` / `case` | no | 3.10 |
| Exception groups | no | 3.11 |
| Type parameter syntax | no | 3.12 |
| FastAPI + SQLAlchemy 2 + Pydantic v2 | yes | 3.10 |
