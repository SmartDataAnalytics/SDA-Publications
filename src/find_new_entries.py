import re
from typing import List, Dict, Set

import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding, latex_to_unicode
from src.get_publication_fetching_data import get_publication_fetching_data

author_ids = map(lambda it: it[2].replace('-', "/"),  get_publication_fetching_data())

existing = "../sda.bib"
blacklist = "blacklist.txt"


def get_candidate_publications():
    ignored_titles = get_ignored_titles()
    candidate_publications = fetch_candidate_publications(ignored_titles)
    print_candidates(candidate_publications)


def get_ignored_titles() -> Set[str]:
    """Returns the titles of publications that we already included in our list or that we explicitly ignore."""

    existing_publications = parse_bibtex_file(existing)
    existing_titles = [
        normalize_title(publication["title"])
        for publication in existing_publications
        if "title" in publication
    ]

    blacklisted_titles = parse_blacklisted_titles()
    print("Blacklisted titles:\n")
    for title in blacklisted_titles:
        print(title)
    print("\n========================================\n")

    ignored_titles = set()
    ignored_titles = ignored_titles.union(existing_titles)
    ignored_titles = ignored_titles.union(blacklisted_titles)

    return ignored_titles

def parse_bibtex_file(path: str) -> List[Dict]:
    with open(path, "r", encoding="UTF-8") as file:
        return create_bibtex_parser().parse_file(file).entries


def create_bibtex_parser() -> BibTexParser:
    bibtex_parser = BibTexParser(common_strings=True)
    bibtex_parser.ignore_nonstandard_types = False
    bibtex_parser.homogenize_fields = True
    bibtex_parser.customization = homogenize_latex_encoding
    return bibtex_parser


def parse_blacklisted_titles() -> Set[str]:
    with (open(blacklist, "r", encoding="UTF-8")) as file:
        return set(map(normalize_title, file))


def normalize_title(title: str) -> str:
    lower_unicode = latex_to_unicode(title).lower()
    no_punctuation = re.sub(r"[-,;:.!?/\\'\"]", " ", lower_unicode)
    normalized_whitespace = re.sub(r"[\n\r\s]+", " ", no_punctuation).strip()
    return normalized_whitespace


def fetch_candidate_publications(ignored_titles: Set[str]) -> List[Dict]:
    result = []
    normalized_title_to_author_ids = {}
    for author_id in author_ids:
        batch = fetch_from_dblp(author_id)
        for entry in batch:
            normalized_title = normalize_title(entry["title"])
            remember_author_id(normalized_title, author_id, normalized_title_to_author_ids)
            if "author" in entry and normalized_title not in ignored_titles:
                result.append(entry)
                ignored_titles.add(normalized_title)

    add_author_ids_as_keywords(result, normalized_title_to_author_ids)

    return result


def fetch_from_dblp(author_id: str) -> List[Dict]:
    bibtex_string = requests.get(f"https://dblp.org/pid/{author_id}.bib").content.decode("utf-8")
    return parse_bibtex_string(bibtex_string)


def parse_bibtex_string(s: str) -> List[Dict]:
    return create_bibtex_parser().parse(s).entries


def remember_author_id(normalized_title: str, author_id: str, normalized_title_to_author_ids: Dict[str, Set]):
    if normalized_title not in normalized_title_to_author_ids:
        normalized_title_to_author_ids[normalized_title] = set()

    author_id_with_hyphen = author_id.replace("/", "-")
    normalized_title_to_author_ids[normalized_title].add(author_id_with_hyphen)


def add_author_ids_as_keywords(publications: List[Dict], normalized_title_to_author_ids: Dict[str, Set]):
    for entry in publications:
        normalized_title = normalize_title(entry["title"])
        author_ids = normalized_title_to_author_ids[normalized_title]

        if "keywords" not in entry:
            entry["keywords"] = ""
        else:
            entry["keywords"] += " "

        entry["keywords"] += " ".join(author_ids)
        entry["keywords"].replace(",", " ")


def print_candidates(candidates: List[Dict]):
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
    get_candidate_publications()
