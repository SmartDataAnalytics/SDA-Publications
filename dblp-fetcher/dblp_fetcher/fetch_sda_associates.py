import logging

from dblp_fetcher.api_wrappers import fetch_data_from_google_sheets, get_credentials
from dblp_fetcher.model import Person
from dblp_fetcher.util import url_from_string, year_from_string

# The ID and range of the DBLP spreadsheet.
_SPREADSHEET_ID = '1YJCn0a30M6aQBra9LgcfrNZ9rGudpjU62SiaBVyFgec'
_RANGE_NAME = 'Data!B2:E'

# Credentials to access the spreadsheet.
_CREDENTIALS_PATH = 'secret/credentials.json'
_TOKEN_PATH = 'secret/token.pickle'


def fetch_sda_associates() -> list[Person]:
    """
    Fetches a list of current and former SDA members from the Google Sheets API.
    """

    data = fetch_data_from_google_sheets(
        spreadsheet_id=_SPREADSHEET_ID,
        range_name=_RANGE_NAME,
        credentials=get_credentials(
            credentials_path=_CREDENTIALS_PATH,
            token_path=_TOKEN_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    )

    if not data:
        logging.error('Error: Could not load DBLP spreadsheet from Google.')
        exit(1)

    return [
        _person_from_spreadsheet_row(author_id, dblp_url, start_year, end_year)
        for [dblp_url, start_year, end_year, author_id] in data
    ]


def _person_from_spreadsheet_row(author_id: str, dblp_url: str, start_year_string: str, end_year_string: str) -> Person:
    """
    Creates a Person from a row in the spreadsheet.
    """

    return Person(
        author_id=author_id,
        dblp_url=url_from_string(dblp_url),
        start_year=year_from_string(start_year_string),
        end_year=year_from_string(end_year_string)
    )
