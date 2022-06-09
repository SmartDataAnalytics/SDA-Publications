import os
import pickle
from typing import Any

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPE_READONLY = 'https://www.googleapis.com/auth/spreadsheets.readonly'


def fetch_data_from_google_sheets(
        spreadsheet_id: str,
        range_name: str,
        credentials: any
) -> list[list[str]]:
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])


def fetch_google_credentials(
        credentials_path: str,
        token_path: str,
        scopes: list[str]
) -> Any:
    result = None

    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            result = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not result or not result.valid:
        if result and result.expired and result.refresh_token:
            result.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            result = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(result, token)

    return result
