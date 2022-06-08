import pytest

from dblp_fetcher.util import is_valid_year


@pytest.mark.parametrize(
    "year_string,expected", [
        ("1900", True),
        ("2019", True),
        ("2100", True),
        ("-1", False),
        ("1899", False),
        ("2101", False),
        ("2019a", False),
    ]
)
def test_is_valid_year(year_string: str, expected: int):
    assert is_valid_year(year_string) == expected
