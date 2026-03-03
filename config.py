import os
import json
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def load_config():
    creds_json = os.environ["CREDENTIALS_FILE"]
    credentials = json.loads(creds_json)

    creds = Credentials.from_service_account_info(
        credentials,
        scopes=SCOPES
    )

    return {
        "creds": creds,
        "spreadsheet_id": os.environ["SPREADSHEET_ID"],
        "range_name": os.environ["RANGE_NAME"],
        "calendar_id": os.environ["CALENDAR_ID"]
    }