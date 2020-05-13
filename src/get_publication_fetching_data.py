import pickle
import os.path
from typing import List

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1YJCn0a30M6aQBra9LgcfrNZ9rGudpjU62SiaBVyFgec'
SAMPLE_RANGE_NAME = 'Data!C2:E'


def get_publication_fetching_data():
    data = fetch_data_from_google()
    if not data:
        print('Error: Could not load the DBLP spreadsheet from Google.')
        exit(1)

    return filter(has_dblp_profile, data)


def fetch_data_from_google():
    service = build('sheets', 'v4', credentials=get_credentials())

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    return result.get('values', [])


def get_credentials():
    token_path = '../secret/token.pickle'
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../secret/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def has_dblp_profile(entry: List) -> bool:
    return len(entry) == 3 and entry[2] != "no profile"


if __name__ == '__main__':
    print(list(get_publication_fetching_data()))
