## Installation

1. Install Python 3.8 or above.
2. Run the following command from the root directory of the repository to install all dependencies:
```
pip install -r src/requirements.txt
```
3. Follow the instructions in Step 1 of the [Google Sheets Python Quickstart guide](https://developers.google.com/sheets/api/quickstart/python) to get a credentials.json file. Save the file as secret/credentials.json relative to the root directory of the repository.
4. **Optional:** If you want to start from scratch:
    * Empty the file sda.bib (contains all valid publications)
    * Empty the file src/blacklist.txt (contains the titles of ignores publications)
    * Change the SAMPLE_SPREADSHEET_ID in src/get_publication_fetching_data.py to the ID of the Google spreadsheet that contains the mapping from people to DBLP IDs. An example for such a spreadsheet can be found under `examples/dblpSpreadsheet.xlsx`.

## Importing new publications

1. Run the following command from the root directory of the repository to fetch new publications:
```
python src/find_new_entries.py
```
2. Check the console output manually to ensure that all new entries are correct.
3. Copy the BibTex output from the console into your tool of choice such as [teachPress](https://wordpress.org/plugins/teachpress/) for WordPress.
