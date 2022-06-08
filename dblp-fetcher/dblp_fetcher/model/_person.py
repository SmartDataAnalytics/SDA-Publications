from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    """
    Parameters
    ----------
    author_id:
        The ID of the author. This is added as a keyword to the author's publications.
    dblp_url:
        The author's DBLP URL. This is used to fetch the author's publications.
    start_year:
        When the author joined SDA. Set to None if unknown.
    end_year:
        When the author left SDA. Set to None if unknown. Set to 9999 if the contract is still active.
    """

    author_id: str
    dblp_url: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None

    def was_sda_member_in_year(self, year: int) -> bool:
        """
        Checks if the person was an SDA member in the given year. Returns False if unknown.
        """

        if self.start_year is None or self.end_year is None:
            return False

        return self.start_year <= year <= self.end_year
