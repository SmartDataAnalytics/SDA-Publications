from dblp_fetcher.persons import fetch_sda_associates

# The ID and range of the DBLP spreadsheet.
from dblp_fetcher.publications import fetch_bibliography
from dblp_fetcher.publications.model import Bibliography

_SPREADSHEET_ID = '1YJCn0a30M6aQBra9LgcfrNZ9rGudpjU62SiaBVyFgec'
_RANGE_NAME = 'Data!B2:E'

# Credentials to access the spreadsheet.
_CREDENTIALS_PATH = 'secret/credentials.json'
_TOKEN_PATH = 'secret/token.pickle'

# Bibtex file with publications we already know.
_KNOWN_PUBLICATION_PATH = "data/sda.bib"

# Text file with titles of publications that should be ignored (e.g. because they are included with a different title).
_BLACKLIST_PATH = "data/blacklist.txt"


def main() -> None:
    # sda_associates = fetch_sda_associates(
    #     spreadsheet_id=_SPREADSHEET_ID,
    #     range_name=_RANGE_NAME,
    #     credentials_path=_CREDENTIALS_PATH,
    #     token_path=_TOKEN_PATH
    # )

    # candidate_publications = fetch_bibliography(sda_associates[0])

    candidate_publications = _read_known_publications()
    print(candidate_publications.to_bibtex())


def _read_known_publications() -> Bibliography:
    with open(_KNOWN_PUBLICATION_PATH, "r", encoding="UTF-8") as bib:
        return Bibliography.from_bibtex(bib.read())

# TODO
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
