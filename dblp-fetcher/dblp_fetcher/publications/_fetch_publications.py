import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding

from dblp_fetcher.persons._fetch_sda_associates import fetch_sda_associates
from dblp_fetcher.util import is_valid_year


# def fetch_publications(author: Person) -> Bibliography:
#     result = Bibliography()
#
#
#
#
#
#
#     normalized_title_to_author_ids = {}
#     sda_publications = set()
#
#     for person in fetch_sda_associates():
#         if not person.has_dblp_profile():
#             continue
#
#         batch = fetch_from_dblp(person.dblp_url)
#         for publication in batch:
#             normalized_title = normalize_title(publication["title"])
#             if skip_publication(publication, normalized_title, ignored_titles):
#                 continue
#
#             remember_author_id(normalized_title, person.author_id, normalized_title_to_author_ids)
#             if is_sda_publication(publication, person):
#                 sda_publications.add(normalized_title)
#
#             if "editor" in publication:
#                 del publication["editor"]
#
#             result.append(Publication(publication))
#             ignored_titles.add(normalized_title)
#
#     add_keywords(result, normalized_title_to_author_ids, sda_publications)
#
#     return Bibliography(result)
#
#
# def fetch_bibtex_from_dblp(dblp_url: str) -> str:
#     return requests.get(f"{dblp_url}.bib").content.decode("utf-8")
#
#
#
# def fetch_publications(authors: List[Person]) -> Bibliography:
#     ignored_titles = get_ignored_titles()
#     candidate_publications = fetch_candidate_publications(ignored_titles)
#     print_candidates(candidate_publications)
#
#     with open(existing, "a") as bib:
#         new_entries = bibtex_entries_to_string(candidate_publications)
#         bib.write(new_entries)
#
#
# def get_ignored_titles() -> Set[str]:
#     """Returns the titles of publications that we already included in our list or that we explicitly ignore."""
#
#     existing_publications = parse_bibtex_file(existing)
#     existing_titles = [
#         normalize_title(publication["title"])
#         for publication in existing_publications
#         if "title" in publication
#     ]
#
#     blacklisted_titles = parse_blacklisted_titles()
#     print("Blacklisted titles:\n")
#     for title in blacklisted_titles:
#         print(title)
#     print("\n========================================\n")
#
#     ignored_titles = set()
#     ignored_titles = ignored_titles.union(existing_titles)
#     ignored_titles = ignored_titles.union(blacklisted_titles)
#
#     return ignored_titles
#
#
# def parse_bibtex_file(path: str) -> List[Dict]:
#     try:
#         with open(path, "r", encoding="UTF-8") as file:
#             return create_bibtex_parser().parse_file(file).entries
#     except IndexError:
#         return []
#
#
# def parse_blacklisted_titles() -> Set[str]:
#     with (open(blacklist, "r", encoding="UTF-8")) as file:
#         return set(map(normalize_title, file))
#
#
# def fetch_candidate_publications(ignored_titles: Set[str]) -> List[Dict]:
#     result = []
#     normalized_title_to_author_ids = {}
#     sda_publications = set()
#
#     for person in fetch_sda_associates():
#         if not person.has_dblp_profile():
#             continue
#
#         batch = fetch_from_dblp(person.dblp_url)
#         for publication in batch:
#             normalized_title = normalize_title(publication["title"])
#             if skip_publication(publication, normalized_title, ignored_titles):
#                 continue
#
#             remember_author_id(normalized_title, person.author_id, normalized_title_to_author_ids)
#             if is_sda_publication(publication, person):
#                 sda_publications.add(normalized_title)
#
#             if "editor" in publication:
#                 del publication["editor"]
#
#             result.append(publication)
#             ignored_titles.add(normalized_title)
#
#     add_keywords(result, normalized_title_to_author_ids, sda_publications)
#
#     return result
#
#
# def skip_publication(publication, normalized_title: str, ignored_titles: Set[str]):
#     return "author" not in publication or normalized_title in ignored_titles or (
#             "archiveprefix" in publication and publication["archiveprefix"].lower() == "arxiv"
#     )
#
#
#
# def fetch_from_dblp(dblp_url: str) -> Bibliography:
#     bibtex_string = requests.get(f"{dblp_url}.bib").content.decode("utf-8")
#     return parse_bibtex_string(bibtex_string)
#
#
# def remember_author_id(normalized_title: str, author_id: str, normalized_title_to_author_ids: Dict[str, Set]):
#     if normalized_title not in normalized_title_to_author_ids:
#         normalized_title_to_author_ids[normalized_title] = set()
#
#     normalized_title_to_author_ids[normalized_title].add(author_id)
#
#
# def is_sda_publication(publication, author: Person) -> bool:
#     if not is_valid_year(publication["year"]):
#         return True
#     publication_year = int(publication["year"])
#
#     return author.was_sda_member_in_year(publication_year)
#
#
# def add_keywords(publications: List[Dict], normalized_title_to_author_ids: Dict[str, Set],
#                  sda_publications: Set[str]):
#     for entry in publications:
#         normalized_title = normalize_title(entry["title"])
#         author_ids = normalized_title_to_author_ids[normalized_title]
#
#         # Add author IDs as keywords
#         if "keywords" not in entry:
#             entry["keywords"] = ""
#         else:
#             entry["keywords"] += " "
#         entry["keywords"] += " ".join(author_ids)
#
#         # Mark SDA publications using a keyword
#         if normalized_title in sda_publications:
#             entry["keywords"] += " " + "sda-pub"
#
#         entry["keywords"].replace(",", " ")
#
#
# def print_candidates(candidates: List[Dict]):
#     count = len(candidates)
#     if count == 0:
#         print("No suggestions.")
#     elif count == 1:
#         print("One suggestion:\n")
#     else:
#         print(f"{count} suggestions:\n")
#
#     output = bibtex_entries_to_string(candidates)
#     print(output)
