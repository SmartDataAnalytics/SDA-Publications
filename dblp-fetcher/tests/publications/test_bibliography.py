from _pytest.fixtures import fixture

from dblp_fetcher.publications.model import Bibliography, Publication


@fixture
def bibtex_string() -> str:
    return """
    @phdthesis{dblp/id,
        title = {{T}itle},
        author = {John Doe},
        year  = {2021},
        keywords = {keyword3 keyword1, keyword2}
    }
    """


@fixture
def bibliography(bibtex_string: str) -> Bibliography:
    return Bibliography.from_bibtex(bibtex_string)


def test_from_bibtex(bibtex_string: str):
    bibliography = Bibliography.from_bibtex(bibtex_string)
    assert len(bibliography.publications) == 1

    publication = bibliography.publications[0]
    assert publication.author == "John Doe"
    assert publication.title == "{T}itle"
    assert publication.year == 2021
    assert publication.keywords == {"keyword1", "keyword2", "keyword3"}


def test_upsert_publication_with_existing_publication(bibliography: Bibliography):
    publication = Publication({
        "title": "{T}itle",
        "year": "2020",
        "keyword": "keyword4 keyword1, keyword2"
    })

    bibliography.upsert_publication(publication)
    assert len(bibliography.publications) == 1

    publication = bibliography.publications[0]
    assert publication.author == "John Doe"
    assert publication.title == "{T}itle"
    assert publication.year == 2020
    assert publication.keywords == {"keyword1", "keyword2", "keyword3", "keyword4"}


def test_upsert_publication_with_new_publication(bibliography: Bibliography):
    publication = Publication({
        "title": "Title 2"
    })

    bibliography.upsert_publication(publication)
    assert len(bibliography.publications) == 2


def test_update(bibliography: Bibliography):
    publication1 = Publication({
        "title": "{T}itle",
        "year": "2020",
        "keyword": "keyword4 keyword1, keyword2"
    })
    publication2 = Publication({
        "title": "Title 2"
    })
    other_bibliography = Bibliography([publication1, publication2])

    bibliography.update(other_bibliography)

    assert len(bibliography.publications) == 2

    publication = bibliography.get_publication_by_id("title")
    assert publication is not None
    assert publication.author == "John Doe"
    assert publication.title == "{T}itle"
    assert publication.year == 2020
    assert publication.keywords == {"keyword1", "keyword2", "keyword3", "keyword4"}


def test_to_bibtex(bibliography: Bibliography):
    assert bibliography.to_bibtex() == """@phdthesis{dblp/id,
  author    = {John Doe},
  keywords  = {keyword1, keyword2, keyword3},
  title     = {{T}itle},
  year      = {2021}
}

"""
