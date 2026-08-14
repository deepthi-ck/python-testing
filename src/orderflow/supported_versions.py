"""All customer Python versions required by Testable / this repository."""

CUSTOMER_VERSIONS = (
    "2.6",
    "2.7",
    "3.4",
    "3.5",
    "3.6",
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
    "3.15",
    "3.16",
)

VERSION_REPO = "https://github.com/deepthi-ck/python-testing"

BRANCH_MAP = dict(("Python_" + version, version) for version in CUSTOMER_VERSIONS)
