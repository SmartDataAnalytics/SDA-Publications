from typing import Optional

import pytest

from dblp_fetcher.util import normalized_title, url_from_string, year_from_string


@pytest.mark.parametrize(
    "title,expected", [
        ("A 'title' - with_special - characters 2020", "atitlewithspecialcharacters2020"),
        ("", "")
    ]
)
def test_normalized_title(title: str, expected: str):
    assert normalized_title(title) == expected


@pytest.mark.parametrize(
    "url_string,expected", [
        ("https://example.org", "https://example.org"),
        ("no profile", None)
    ]
)
def test_url_from_string(url_string: str, expected: Optional[str]):
    assert url_from_string(url_string) == expected


@pytest.mark.parametrize(
    "year_string,expected", [
        ("2019", 2019),
        ("2019a", None)
    ]
)
def test_year_from_string(year_string: str, expected: Optional[int]):
    assert year_from_string(year_string) == expected
