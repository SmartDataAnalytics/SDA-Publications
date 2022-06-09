from dataclasses import dataclass, field


@dataclass
class TitleBlacklist:
    """
    Parameters
    ----------
    blacklist:
        The set of blacklisted titles.
    """

    blacklist: set[str] = field(default_factory=set)

    def add(self, title: str):
        """
        Adds the given title to the blacklist.
        """

        self.blacklist.add(title)

    def is_blacklisted(self, title: str) -> bool:
        """
        Checks if the given title is blacklisted.
        """

        return title in self.blacklist
