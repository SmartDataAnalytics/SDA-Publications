import pytest
from _pytest.fixtures import fixture

from dblp_fetcher.publications.model import TitleBlacklist


@fixture
def blacklist() -> TitleBlacklist:
    return TitleBlacklist(["A 'title' - with_special - characters 2020"])


@pytest.mark.parametrize(
    "title,expected", [
        ("A 'title' - with_special - characters 2020", True),
        ("A 'title' - with_special - characters 2020 ?", True),
        ("atitlewithspecialcharacters2020", True),
        ("", False)
    ]
)
def test_is_blacklisted(title: str, expected: bool, blacklist: TitleBlacklist):
    assert blacklist.is_blacklisted(title) == expected
