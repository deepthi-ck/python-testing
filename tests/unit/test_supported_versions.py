"""All 15 Testable customer Python versions stay registered."""
import pytest

from orderflow.supported_versions import BRANCH_MAP, CUSTOMER_VERSIONS, VERSION_REPO


@pytest.mark.unit
def test_all_python_testing_versions_are_registered() -> None:
    expected = (
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
    assert CUSTOMER_VERSIONS == expected
    assert len(BRANCH_MAP) == 15
    assert BRANCH_MAP["Python_2.6"] == "2.6"
    assert BRANCH_MAP["Python_3.16"] == "3.16"
    assert VERSION_REPO == "https://github.com/deepthi-ck/python-testing"
