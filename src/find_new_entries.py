import re
from typing import List, Dict, Set

import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding, latex_to_unicode

# See https://dblp.org/faq/How+can+I+fetch+all+publications+of+one+specific+author on how to obtain these URLs.
author_urls = [
    "https://dblp.org/pid/71/4882.bib",  # Jens Lehmann
]

existing = "../sda.bib"
blacklist = "blacklist.txt"


def getCandidatePublications():
    ignored_titles = getIgnoredTitles()
    candidate_publications = fetchCandidatePublications(ignored_titles)
    printCandidates(candidate_publications)


def getIgnoredTitles() -> Set[str]:
    """Returns the titles of publications that we already included in our list or that we explicitly ignore."""

    existing_publications = parseBibtexFile(existing)
    existing_titles = [
        normalizeTitle(publication["title"])
        for publication in existing_publications
        if "title" in publication
    ]

    blacklisted_titles = parseBlacklistedTitles()

    ignored_titles = set()
    ignored_titles = ignored_titles.union(existing_titles)
    ignored_titles = ignored_titles.union(blacklisted_titles)

    return ignored_titles


def parseBibtexFile(path: str) -> List[Dict]:
    with open(path, "r", encoding="UTF-8") as file:
        return createBibtexParser().parse_file(file).entries


def createBibtexParser() -> BibTexParser:
    bibtex_parser = BibTexParser(common_strings=True)
    bibtex_parser.ignore_nonstandard_types = False
    bibtex_parser.homogenize_fields = True
    bibtex_parser.customization = homogenize_latex_encoding
    return bibtex_parser


def parseBlacklistedTitles() -> Set[str]:
    with (open(blacklist, "r", encoding="UTF-8")) as file:
        return set(map(normalizeTitle, file))


def normalizeTitle(title: str) -> str:
    unicode = latex_to_unicode(title)

    intermediate = unicode \
        .strip() \
        .lower() \
        .replace("---", "-") \
        .replace("--", "-")

    return re.sub(r"[\n\r\s]+", " ", intermediate)


def fetchCandidatePublications(ignored_titles: Set[str]) -> List[Dict]:
    result = []
    for url in author_urls:
        batch = fetchFromDBLP(url)
        for entry in batch:
            normalized_title = normalizeTitle(entry["title"])
            if "author" in entry and normalized_title not in ignored_titles:
                result.append(entry)
                ignored_titles.add(normalized_title)
    return result


def fetchFromDBLP(url: str) -> List[Dict]:
    bibtex_string = requests.get(url).content.decode("utf-8")
    return parseBibtexString(bibtex_string)


def parseBibtexString(s: str) -> List[Dict]:
    return createBibtexParser().parse(s).entries


def printCandidates(candidates: List[Dict]):
    writer = BibTexWriter()
    writer.align_values = True
    writer.indent = "  "

    db = BibDatabase()
    db.entries = candidates

    print(f"{len(candidates)} suggestions:\n")

    output = writer.write(db)
    print(output)


if __name__ == '__main__':
    getCandidatePublications()
