from googleapiclient.discovery import build
from datetime import datetime,timedelta, timezone

def get_calendar_service(creds):
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_sheet_service(creds):
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

from datetime import datetime, timedelta, timezone

def get_today_events(calendar_service, calendarId):
    now = datetime.now(timezone.utc)

    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    print("TimeMin:", start_of_day.isoformat())
    print("TimeMax:", end_of_day.isoformat())

    events_result = calendar_service.events().list(
        calendarId=calendarId,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])


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


def date_exists(sheet, spreadsheet_id, sheet_name, date_str):
    """Check if a date already exists in column A of the given sheet."""
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:A"  # look only in column A
    ).execute()
    values = result.get('values', [])
    
    # Flatten the list and compare
    existing_dates = [row[0] for row in values if row]
    return date_str in existing_dates


def ensure_month_sheet_exists(service, spreadsheet_id, month_name):
    """Check if a sheet with month_name exists, if not, create it."""
    sheets = service.get(spreadsheetId=spreadsheet_id).execute().get('sheets', [])
    sheet_titles = [s['properties']['title'] for s in sheets]
    
    if month_name not in sheet_titles:
        requests = [{
            "addSheet": {
                "properties": {
                    "title": month_name
                }
            }
        }]
        response = service.batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": requests}).execute()
        sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        # Add header row
        header_body = {'values': [["Date", "Start", "End", "Total Hours", "Monthly Total"]]}
        service.values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{month_name}!A1:E1",
            valueInputOption='RAW',
            body=header_body
        ).execute()

       
         # Style header row
        format_request = {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex":0, "endRowIndex":1},
                "cell": {"userEnteredFormat": {
                    "backgroundColor": {"red":0.8,"green":0.8,"blue":0.8},
                    "horizontalAlignment": "CENTER",
                    "textFormat": {"bold": True,"fontSize": 12,"foregroundColor":{"red":0,"green":0,"blue":0}}
                }},
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        }

        # Add borders for first 1000 rows
        border_request = {
            "updateBorders": {
                "range": {"sheetId": sheet_id, "startRowIndex":0, "endRowIndex":1000, "startColumnIndex":0, "endColumnIndex":5},
                "top":{"style":"SOLID"}, "bottom":{"style":"SOLID"}, "left":{"style":"SOLID"}, "right":{"style":"SOLID"},
                "innerHorizontal":{"style":"SOLID"}, "innerVertical":{"style":"SOLID"}
            }
        }

        # Add Monthly Total formula in E2 using =SUM(D:D)
        formula_request = {
            "updateCells": {
                "range": {"sheetId": sheet_id, "startRowIndex":1, "endRowIndex":2, "startColumnIndex":4, "endColumnIndex":5},
                "rows":[{"values":[{"userEnteredValue":{"formulaValue":"=SUM(D:D)"}}]}],
                "fields":"userEnteredValue"
            }
        }

        service.batchUpdate(spreadsheetId=spreadsheet_id, body={"requests":[format_request, border_request, formula_request]}).execute()
        print(f"Created new sheet with formatting and Monthly Total: {month_name}")

