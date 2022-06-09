from __future__ import annotations

import re
from typing import Optional, Any

from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding
from bibtexparser.latexenc import latex_to_unicode

from dblp_fetcher.util import year_from_string


class Bibliography:
    """
    Parameters
    ----------
    publications:
        The initial list of publications in this bibliography.
    """

    @staticmethod
    def from_bibtex(bibtex_string: str) -> Bibliography:
        """
        Parses a bibtex string and returns a bibliography.
        """

        bibtex_dicts: list[dict[str, str]] = _create_bibtex_parser().parse(bibtex_string).entries
        publications: list[Publication] = [Publication(bibtex_dict) for bibtex_dict in bibtex_dicts]
        return Bibliography(publications)

    def __init__(self, publications: list[Publication]):
        self._publications: dict[str, Publication] = {}
        for publication in publications:
            self.upsert_publication(publication)

    @property
    def publications(self) -> list[Publication]:
        """
        Returns a list of all publications in this bibliography. Publications are not copied, so any changes made to
        them are reflected in the bibliography.
        """

        return list(self._publications.values())

    def upsert_publication(self, publication: Publication) -> Bibliography:
        """
        Inserts a publication into this bibliography if no other publication with the same ID exists yet. Otherwise,
        updates the existing publication. Returns this bibliography.
        """

        pass

    def to_bibtex(self) -> str:
        """
        Returns a bibtex string representation of this bibliography.
        """

        if len(self._publications) == 0:
            return ""

        db = BibDatabase()
        db.entries = [publication.bibtex_dict for publication in self._publications.values()]

        return _create_bibtex_writer().write(db)


class Publication:
    def __init__(self, bibtex_dict: dict[str, str]):
        self.bibtex_dict: dict[str, str] = bibtex_dict
        self._normalize_keywords()

    @property
    def archiveprefix(self) -> Optional[str]:
        return self.bibtex_dict.get("archiveprefix")

    @property
    def author(self) -> Optional[str]:
        return self.bibtex_dict.get("author")

    @property
    def id(self) -> Optional[str]:
        if self.title is None:
            return None

        lower_unicode = latex_to_unicode(self.title).lower()
        letters_only = re.sub(r"[^a-z\d]", "", lower_unicode)
        return letters_only

    @property
    def keywords(self) -> set[str]:
        keywords_string = self.bibtex_dict.get("keywords")
        if keywords_string is None:
            return set()

        keyword_list = re.split(r",", keywords_string)
        non_empty_keyword_list = [keyword for keyword in keyword_list if keyword != ""]
        return set(non_empty_keyword_list)

    @property
    def title(self) -> Optional[str]:
        return self.bibtex_dict.get("title")

    @property
    def year(self) -> Optional[int]:
        year_string = self.bibtex_dict.get("year")
        if year_string is None:
            return None

        return year_from_string(year_string)

    def add_keyword(self, keyword: str) -> Publication:
        """
        Adds a keyword to this publication. Returns this publication.
        """

        keyword_set = self.keywords
        keyword_set.add(keyword)
        self.bibtex_dict["keywords"] = ",".join(keyword_set)

        return self

    def remove_property(self, key: str) -> Publication:
        """
        Removes the property with the given key. Returns this publication.
        """

        if key in self.bibtex_dict:
            del self.bibtex_dict[key]

        return self

    def update(self, other: Publication) -> Publication:
        """
        Updates this publication with the properties of the other publication. Returns this publication.
        """

        # Keywords are merged, everything else is overwritten.
        old_keywords = self.keywords
        self.bibtex_dict.update(other.bibtex_dict)
        for keyword in old_keywords:
            self.add_keyword(keyword)

        return self

    def _normalize_keywords(self) -> None:
        """
        Ensures the keyword property exists and that keywords are separated by commas.
        """

        keywords_string = self.bibtex_dict.get("keywords", "")
        keywords_string = re.sub(r"\s", ",", keywords_string)
        keywords_string = re.sub(r",+", ",", keywords_string)
        self.bibtex_dict["keywords"] = keywords_string


def _create_bibtex_parser() -> BibTexParser:
    """
    Returns a BibTexParser instance with custom settings.
    """

    bibtex_parser = BibTexParser(common_strings=True)
    bibtex_parser.ignore_nonstandard_types = False
    bibtex_parser.homogenize_fields = True
    bibtex_parser.customization = homogenize_latex_encoding
    return bibtex_parser


def _create_bibtex_writer() -> BibTexWriter:
    """
    Returns a BibTexWriter instance with custom settings.
    """

    writer = BibTexWriter()
    writer.align_values = True
    writer.indent = "  "
    return writer
