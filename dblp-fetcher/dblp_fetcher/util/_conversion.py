import re
from typing import Optional

from bibtexparser.latexenc import latex_to_unicode
from validators.url import url as is_url

from ._validation import is_valid_year


def normalized_title(title: str) -> str:
    """
    Returns a normalized version of the given title. Particularly, special characters are removed.
    """

    lower_unicode = latex_to_unicode(title).lower()
    letters_only = re.sub(r"[^a-z\d]", "", lower_unicode)
    return letters_only


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
