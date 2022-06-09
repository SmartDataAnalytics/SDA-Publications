import logging

from ._person import Person
from dblp_fetcher.util import url_from_string, year_from_string, fetch_data_from_google_sheets, fetch_google_credentials


def fetch_sda_associates(
        spreadsheet_id: str,
        range_name: str,
        credentials_path: str,
        token_path: str
) -> list[Person]:
    """
    Fetches a list of current and former SDA members from the Google Sheets API.
    """

    data = fetch_data_from_google_sheets(
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        credentials=fetch_google_credentials(
            credentials_path=credentials_path,
            token_path=token_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    )

    if not data:
        logging.error('Error: Could not load DBLP spreadsheet from Google.')
        exit(1)

    return [
        _person_from_spreadsheet_row(dblp_url, start_year, end_year, author_id)
        for [dblp_url, start_year, end_year, author_id] in data
    ]


def _person_from_spreadsheet_row(dblp_url: str, start_year_string: str, end_year_string: str, author_id: str) -> Person:
    """
    Creates a Person from a row in the spreadsheet.
    """

    return Person(
        author_id=author_id,
        dblp_url=url_from_string(dblp_url),
        start_year=year_from_string(start_year_string),
        end_year=year_from_string(end_year_string)
    )
