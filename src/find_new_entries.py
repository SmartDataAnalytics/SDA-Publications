import re
from typing import List, Dict, Set, Any

import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding, latex_to_unicode

from src.get_publication_fetching_data import get_publication_fetching_data

# To run this script, you need to download a file credentials.json from
# https://developers.google.com/sheets/api/quickstart/python and put it into the folder "secret" on the same level as the
# "src" folder.

publication_fetching_data = get_publication_fetching_data()

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
    sda_publications = set()

    for entry in publication_fetching_data:
        start_year, end_year, author_id = entry[0], entry[1], entry[2]

        batch = fetch_from_dblp(author_id)
        for publication in batch:
            normalized_title = normalize_title(publication["title"])

            remember_author_id(normalized_title, author_id, normalized_title_to_author_ids)
            if is_sda_publication(publication, start_year, end_year):
                sda_publications.add(normalized_title)

            if "author" in publication and normalized_title not in ignored_titles:
                result.append(publication)
                ignored_titles.add(normalized_title)

    add_author_ids_as_keywords(result, normalized_title_to_author_ids, sda_publications)

    return result


def fetch_from_dblp(author_id: str) -> List[Dict]:
    author_path = author_id.replace("-", "/")
    bibtex_string = requests.get(f"https://dblp.org/pid/{author_path}.bib").content.decode("utf-8")
    return parse_bibtex_string(bibtex_string)


def parse_bibtex_string(s: str) -> List[Dict]:
    return create_bibtex_parser().parse(s).entries


def remember_author_id(normalized_title: str, author_id: str, normalized_title_to_author_ids: Dict[str, Set]):
    if normalized_title not in normalized_title_to_author_ids:
        normalized_title_to_author_ids[normalized_title] = set()

    normalized_title_to_author_ids[normalized_title].add(author_id)


def is_sda_publication(publication, start_year_string: str, end_year_string: str) -> bool:
    if not is_valid_year(publication["year"]):
        return True

    publication_year = int(publication["year"])
    start_year = int(start_year_string) if is_valid_year(start_year_string) else 0
    end_year = int(end_year_string) if is_valid_year(end_year_string) else 9999

    return start_year <= publication_year <= end_year


def is_valid_year(value: Any) -> bool:
    return type(value) == str and value.isnumeric()


def add_author_ids_as_keywords(publications: List[Dict], normalized_title_to_author_ids: Dict[str, Set],
                               sda_publications: Set[str]):
    for entry in publications:
        normalized_title = normalize_title(entry["title"])
        author_ids = normalized_title_to_author_ids[normalized_title]

        # Add author IDs as keywords
        if "keywords" not in entry:
            entry["keywords"] = ""
        else:
            entry["keywords"] += " "
        entry["keywords"] += " ".join(author_ids)

        # Mark SDA publications using a keyword
        if normalized_title in sda_publications:
            entry["keywords"] += " " + "sda-pub"

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
