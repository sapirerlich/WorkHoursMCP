from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheet_service(credentials_file):
    creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def insert_event(sheet, spreadsheet_id, range_name, event, total_hours):
    values = [[event['date'], event['start'], event['end'], round(total_hours, 2)]]
    body = {'values': values}
    sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"Inserted: {event['date']} | {event['start']}-{event['end']} | {total_hours:.2f} hours")
