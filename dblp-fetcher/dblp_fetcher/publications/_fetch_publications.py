import requests

from dblp_fetcher.persons.model import Person
from dblp_fetcher.publications.model import Bibliography, Publication


def fetch_bibliography(author: Person) -> Bibliography:
    if not author.has_dblp_profile():
        return Bibliography()

    bibtex_string = _fetch_bibtex_from_dblp(author.dblp_url)
    bibliography = Bibliography.from_bibtex(bibtex_string)

    for publication in bibliography.publications:
        _add_keywords(publication, author)

    return bibliography


def _fetch_bibtex_from_dblp(dblp_url: str) -> str:
    return requests.get(f"{dblp_url}.bib").content.decode("utf-8")


def _add_keywords(publication: Publication, author: Person) -> None:
    """
    Add author ID as keyword and "sda-pub" if the author was an SDA member at the time of the publication.
    """

    publication.add_keyword(author.author_id)

    if _is_sda_publication(publication, author):
        publication.add_keyword("sda-pub")


def _is_sda_publication(publication: Publication, author: Person) -> bool:
    """
    Whether the publication was written while the author was an SDA member.
    """

    publication_year = publication.year
    return publication_year is not None and author.was_sda_member_in_year(publication_year)
