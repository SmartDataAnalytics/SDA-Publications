from typing import Optional

from dblp_fetcher.find_new_entries import is_valid_year


def year_from_string(year_string: str) -> Optional[int]:
    """
    Converts a string to a year. If the string is not a valid year, returns None.
    """

    return int(year_string) if is_valid_year(year_string) else None
