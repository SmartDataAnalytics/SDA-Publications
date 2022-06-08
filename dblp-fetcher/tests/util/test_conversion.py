import pytest

from dblp_fetcher.util import year_from_string
from dblp_fetcher.util import url_from_string


@pytest.mark.parametrize(
    "year_string,expected", [
        ("2019", 2019),
        ("2019a", None)
    ]
)
def test_year_from_string(year_string: str, expected: int):
    assert year_from_string(year_string) == expected


@pytest.mark.parametrize(
    "url_string,expected", [
        ("https://example.org", "https://example.org"),
        ("no profile", None)
    ]
)
def test_url_from_string(url_string: str, expected: int):
    assert url_from_string(url_string) == expected
