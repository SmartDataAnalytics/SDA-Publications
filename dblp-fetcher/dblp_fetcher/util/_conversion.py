from typing import Optional

from validators.url import url as is_url

from ._validation import is_valid_year


def url_from_string(url_string: str) -> Optional[str]:
    """
    Converts a string to a URL (still as a string). If the string is not a valid URL, returns None.
    """

    return url_string if is_url(url_string) else None


def year_from_string(year_string: str) -> Optional[int]:
    """
    Converts a string to a year. If the string is not a valid year, returns None.
    """

    return int(year_string) if is_valid_year(year_string) else None
