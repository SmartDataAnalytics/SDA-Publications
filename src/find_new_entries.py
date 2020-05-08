import re
from typing import List, Dict, Set

import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding, latex_to_unicode

# See https://dblp.org/faq/How+can+I+fetch+all+publications+of+one+specific+author on how to obtain these URLs.
author_urls = [
    "https://dblp.org/pid/71/4882",  # Jens Lehmann
    "https://dblp.org/pid/180/1858",  # Mohnish Dubey
    "https://dblp.org/pid/143/9337",  # Patrick Westphal
    "https://dblp.org/pid/185/1477",  # Fathoni Musyaffa
    "https://dblp.org/pid/205/3220",  # Said Fathalla
    "https://dblp.org/pid/183/0983",  # Tobias Grubenmann
    "https://dblp.org/pid/160/8154",  # Mikhail Galkin
    "https://dblp.org/pid/187/1650",  # Najmeh
    "https://dblp.org/pid/228/9241",  # Shimaa Ibrahim
    "https://dblp.org/pid/143/6365",  # Elisa Sibarani
    "https://dblp.org/pid/213/7337",  # Debanjan Chaudhuri
    "https://dblp.org/pid/160/8802",  # Priyansh Trivedi
    "https://dblp.org/pid/67/10152",  # Gaurav Maheshwari
    "https://dblp.org/pid/251/0778",  # Md Rashad Al Hasan Rony
    "https://dblp.org/pid/227/6127",  # Mayesha Tasnim
    "https://dblp.org/pid/65/9656",  # Ricardo Usbeck
    "https://dblp.org/pid/162/8992",  # Liubov Kovriguina
    "https://dblp.org/pid/169/3503"  # Klaudia Thellmann
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
    print("Blacklisted titles:\n")
    for title in blacklisted_titles:
        print(title)
    print("\n========================================\n")

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
    lower_unicode = latex_to_unicode(title).lower()
    no_punctuation = re.sub(r"[-,;:.!?/\\'\"]", " ", lower_unicode)
    normalized_whitespace = re.sub(r"[\n\r\s]+", " ", no_punctuation).strip()
    return normalized_whitespace


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
    bibtex_string = requests.get(f"{url}.bib").content.decode("utf-8")
    return parseBibtexString(bibtex_string)


def parseBibtexString(s: str) -> List[Dict]:
    return createBibtexParser().parse(s).entries


def printCandidates(candidates: List[Dict]):
    count = len(candidates)
    if count == 0:
        print("No suggestions.")
    else:
        if count == 1:
            print("One suggestion:\n")
        else:
            print(f"{count} suggestions:\n")

        writer = BibTexWriter()
        writer.align_values = True
        writer.indent = "  "

        db = BibDatabase()
        db.entries = candidates

        output = writer.write(db)
        print(output)


if __name__ == '__main__':
    getCandidatePublications()
