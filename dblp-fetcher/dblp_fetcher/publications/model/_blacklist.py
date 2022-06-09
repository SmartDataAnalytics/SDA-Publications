from dataclasses import dataclass, field

from dblp_fetcher.util import normalized_title


class TitleBlacklist:
    """
    Parameters
    ----------
    blacklist:
        The set of blacklisted titles.
    """

    def __init__(self, blacklist: list[str] = None):
        if blacklist is None:
            blacklist = list()

        self._blacklist: set[str] = set()

        for title in blacklist:
            self.add(title)

    _blacklist: set[str] = field(default_factory=set)

    def add(self, title: str):
        """
        Adds the given title to the blacklist.
        """

        self._blacklist.add(normalized_title(title))

    def is_blacklisted(self, title: str) -> bool:
        """
        Checks if the given title is blacklisted.
        """

        return normalized_title(title) in self._blacklist
