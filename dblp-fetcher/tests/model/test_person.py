import pytest

from dblp_fetcher.model import Person


@pytest.mark.parametrize(
    "person,year,expected", [
        (
                Person("person", "person", start_year=2019, end_year=2021),
                2018,
                False
        ),
        (
                Person("person", "person", start_year=2019, end_year=2021),
                2019,
                True
        ),
        (
                Person("person", "person", start_year=2019, end_year=2021),
                2020,
                True
        ),
        (
                Person("person", "person", start_year=2019, end_year=2021),
                2021,
                True
        ),
        (
                Person("person", "person", start_year=2019, end_year=2021),
                2022,
                False
        ),
        (
                Person("person", "person", start_year=2019, end_year=None),
                2020,
                True
        ),
        (
                Person("person", "person", start_year=None, end_year=2021),
                2020,
                False
        ),
        (
                Person("person", "person", start_year=None, end_year=None),
                2020,
                False
        ),
    ]
)
def test_was_sda_member_in_year(person: Person, year: int, expected: bool):
    assert person.was_sda_member_in_year(year) == expected
