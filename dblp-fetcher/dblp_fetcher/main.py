from dblp_fetcher.persons import fetch_sda_associates

# The ID and range of the DBLP spreadsheet.
_SPREADSHEET_ID = '1YJCn0a30M6aQBra9LgcfrNZ9rGudpjU62SiaBVyFgec'
_RANGE_NAME = 'Data!B2:E'

# Credentials to access the spreadsheet.
_CREDENTIALS_PATH = 'secret/credentials.json'
_TOKEN_PATH = 'secret/token.pickle'

# Bibtex file with publications we already know.
_EXISTING_PUBLICATION_PATH = "data/sda.bib"

# Text file with titles of publications that should be ignored (e.g. because they are included with a different title).
_BLACKLIST_PATH = "data/blacklist.txt"


def main() -> None:
    sda_associates = fetch_sda_associates(
        spreadsheet_id=_SPREADSHEET_ID,
        range_name=_RANGE_NAME,
        credentials_path=_CREDENTIALS_PATH,
        token_path=_TOKEN_PATH
    )

    for person in sda_associates:
        print(person)

    # candidate_publications = fetch_publications(sda_associates)
