## Installation

1. Install Python 3.10.
2. Install [poetry](https://python-poetry.org/docs/master/#installation).
3. **Only the first time**, install dependencies:
```sh
cd dblp-fetcher
poetry install
```
4. Follow the instructions in Step 1 of the [Google Sheets Python Quickstart guide](https://developers.google.com/sheets/api/quickstart/python) to get a credentials.json file. Save the file as secret/credentials.json relative to the root directory of the repository.

## Importing new publications

1. Run the following command from the root directory of the repository to fetch new publications:
```sh
cd dblp-fetcher
poetry run dblp-fetcher
```
2. Check the console output manually to ensure that all new entries are correct.
3. Copy the BibTex output from the console into your tool of choice such as [teachPress](https://wordpress.org/plugins/teachpress/) for WordPress.
