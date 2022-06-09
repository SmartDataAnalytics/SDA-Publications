from _pytest.fixtures import fixture

from dblp_fetcher.persons.model import Person
from dblp_fetcher.publications import fetch_bibliography


@fixture
def person() -> Person:
    return Person(
        author_id="272-2782",
        start_year=0,
        end_year=9999,
        dblp_url="https://dblp.org/pid/272/2782"
    )


def test_fetch_bibliography_with_dblp_profile(person: Person):
    bibliography = fetch_bibliography(person)

    assert len(bibliography.publications) > 0
    for publication in bibliography.publications:
        assert person.author_id in publication.keywords
        assert "sda-pub" in publication.keywords


def test_fetch_bibliography_with_no_dblp_profile():
    person = Person(author_id="272-2782", dblp_url=None)

    bibliography = fetch_bibliography(person)

    assert len(bibliography.publications) == 0
