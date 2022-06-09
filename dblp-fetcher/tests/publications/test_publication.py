from _pytest.fixtures import fixture

from dblp_fetcher.publications.model import Publication


@fixture
def complete_publication() -> Publication:
    return Publication({
        "author": "John Doe",
        "title": "A 'title' - with_special - characters 2020",
        "year": "2020",
        "keyword": "keyword3 keyword1, keyword2",
        "archiveprefix": "arxiv",
    })


@fixture
def empty_publication() -> Publication:
    return Publication({})


def test_init_normalizes_keywords(complete_publication: Publication):
    assert complete_publication.bibtex_dict["keywords"] == "keyword1, keyword2, keyword3"


def test_archiveprefix_complete(complete_publication: Publication):
    assert complete_publication.archiveprefix == "arxiv"


def test_archiveprefix_empty(empty_publication: Publication):
    assert empty_publication.archiveprefix is None


def test_author_complete(complete_publication: Publication):
    assert complete_publication.author == "John Doe"


def test_author_empty(empty_publication: Publication):
    assert empty_publication.author is None


def test_id_complete(complete_publication: Publication):
    # noinspection SpellCheckingInspection
    assert complete_publication.id == "atitlewithspecialcharacters2020"


def test_id_empty(empty_publication: Publication):
    assert empty_publication.id is None


def test_keywords_complete(complete_publication: Publication):
    assert complete_publication.keywords == {"keyword1", "keyword2", "keyword3"}


def test_keywords_empty(empty_publication: Publication):
    assert empty_publication.keywords == set()


def test_title_complete(complete_publication: Publication):
    assert complete_publication.title == "A 'title' - with_special - characters 2020"


def test_title_empty(empty_publication: Publication):
    assert empty_publication.title is None


def test_year_complete(complete_publication: Publication):
    assert complete_publication.year == 2020


def test_year_empty(empty_publication: Publication):
    assert empty_publication.year is None


def test_add_keyword_with_existing_keyword(complete_publication: Publication):
    complete_publication.add_keyword("keyword1")
    assert complete_publication.keywords == {"keyword1", "keyword2", "keyword3"}
    assert complete_publication.bibtex_dict.get("keywords") == "keyword1, keyword2, keyword3"


def test_add_keyword_with_new_keyword(empty_publication: Publication):
    empty_publication.add_keyword("keyword1")
    assert empty_publication.keywords == {"keyword1"}
    assert empty_publication.bibtex_dict.get("keywords") == "keyword1"


def test_remove_property_with_existing_property(complete_publication: Publication):
    complete_publication.remove_property("year")
    assert complete_publication.year is None


def test_remove_property_with_missing_property(empty_publication: Publication):
    empty_publication.remove_property("year")
    assert empty_publication.year is None


def test_update(complete_publication: Publication):
    other = Publication({
        "author": "Jane Doe",
        "title": "A better title",
        "year": "2022",
        "keywords": "keyword1, keyword3, keyword4"
    })

    complete_publication.update(other)

    assert complete_publication.author == "Jane Doe"
    assert complete_publication.title == "A better title"
    assert complete_publication.year == 2022
    assert complete_publication.keywords == {"keyword1", "keyword2", "keyword3", "keyword4"}
    assert complete_publication.archiveprefix == "arxiv"
