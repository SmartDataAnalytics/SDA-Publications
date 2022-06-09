import logging

from dblp_fetcher.persons import fetch_sda_associates

# The ID and range of the DBLP spreadsheet.
from dblp_fetcher.publications import fetch_bibliography
from dblp_fetcher.publications.model import Bibliography, TitleBlacklist, Publication

_SPREADSHEET_ID = '1YJCn0a30M6aQBra9LgcfrNZ9rGudpjU62SiaBVyFgec'
_RANGE_NAME = 'Data!B2:E'

# Credentials to access the spreadsheet.
_CREDENTIALS_PATH = 'secret/credentials.json'
_TOKEN_PATH = 'secret/token.pickle'

# Bibtex file with publications we already know.
_KNOWN_PUBLICATION_PATH = "data/sda.bib"

# Text file with titles of publications that should be ignored (e.g. because they are included with a different title).
_BLACKLIST_PATH = "data/blacklist.txt"


def main() -> None:
    # Fetch all SDA associates.
    logging.info("Fetching SDA associates...")
    sda_associates = fetch_sda_associates(
        spreadsheet_id=_SPREADSHEET_ID,
        range_name=_RANGE_NAME,
        credentials_path=_CREDENTIALS_PATH,
        token_path=_TOKEN_PATH
    )

    # Update bibliography
    logging.info("Parsing known publications...")
    complete_bibliography = _read_known_publications()

    for sda_associate in sda_associates:
        logging.info(f"Fetching publications for {sda_associate.author_id}...")
        associate_bibliography = fetch_bibliography(sda_associate)
        complete_bibliography.update(associate_bibliography)

    # Postprocess bibliography
    logging.info("Postprocessing bibliography...")
    _postprocess_bibliography(complete_bibliography)

    # Write bibliography to file
    logging.info("Writing updated bibliography to file...")
    _write_updated_bibliography(complete_bibliography)


def _read_known_publications() -> Bibliography:
    """
    Reads the known publications from the file.
    """

    with open(_KNOWN_PUBLICATION_PATH, "r", encoding="UTF-8") as bib:
        return Bibliography.from_bibtex(bib.read())


def _postprocess_bibliography(bibliography: Bibliography) -> None:
    _remove_unwanted_publications(bibliography)
    _remove_editor_property(bibliography)


def _remove_unwanted_publications(bibliography: Bibliography) -> None:
    blacklist = _read_blacklist()

    for publication in bibliography.publications:
        if _is_unwanted(publication, blacklist):
            bibliography.remove_publication_by_id(publication.id)


def _is_unwanted(publication: Publication, blacklist: TitleBlacklist) -> bool:
    """
    Returns whether the given publication is unwanted. This is the case if the publication has no author or title, if
    the title is blacklisted, or if the publication is an Arxiv preprint.
    """

    return publication.author is None or publication.title is None or blacklist.is_blacklisted(publication.title) or \
           _is_arxiv_preprint(publication)


def _is_arxiv_preprint(publication: Publication) -> bool:
    archive = publication.archiveprefix
    return archive is not None and archive.lower() == "arxiv"


def _read_blacklist() -> TitleBlacklist:
    """
    Reads titles from the blacklist file.
    """

    with open(_BLACKLIST_PATH, "r", encoding="UTF-8") as blacklist:
        return TitleBlacklist(list(line.strip() for line in blacklist))


def _remove_editor_property(bibliography) -> None:
    """
    Removes the editor property from all publications.
    """

    for publication in bibliography.publications:
        publication.remove_property("editor")


def _write_updated_bibliography(bibliography: Bibliography) -> None:
    with open(_KNOWN_PUBLICATION_PATH, "w", encoding="UTF-8") as bib:
        bib.write(bibliography.to_bibtex())
