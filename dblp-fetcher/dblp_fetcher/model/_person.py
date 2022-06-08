from __future__ import annotations

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
        The author's DBLP URL. This is used to fetch the author's publications. Set to None if unknown.
    start_year:
        When the author joined SDA. Set to None if unknown.
    end_year:
        When the author left SDA. Set to None if unknown.
    """

    author_id: str
    dblp_url: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

    def has_dblp_profile(self) -> bool:
        """
        Checks if the author has a DBLP profile.
        """

        return self.dblp_url is not None

    def was_sda_member_in_year(self, year: int) -> bool:
        """
        Checks if the person was an SDA member in the given year. Returns False if start_year is unknown. If the
        end_year is unknown, the contract is assumed to still be active.
        """

        if self.start_year is None:
            return False

        end_year = 9999 if self.end_year is None else self.end_year

        return self.start_year <= year <= end_year
