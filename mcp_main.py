import json
import schedule
import time
from datetime import datetime
from sheets_helper import get_sheet_service, insert_event, ensure_month_sheet_exists
import calendar


# ----- Setup Google Sheets -----
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1pLd3IXbDggq2gdmgFGuVvaFqQ74joEwx7zpiZgvgyOA'
RANGE_NAME = 'Sheet1!A:D'  

# Load dummy events
with open('dummy_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

sheet = get_sheet_service(CREDENTIALS_FILE)

def process_work_events():
    print("Checking for work events...")
    for event in events:
        if "work" in event['title']:
            fmt = "%H:%M"
            start_dt = datetime.strptime(event['start'], fmt)
            end_dt = datetime.strptime(event['end'], fmt)
            total_hours = (end_dt - start_dt).seconds / 3600
            # Month name from event date
            event_date = datetime.strptime(event['date'], "%Y-%m-%d")
            month_name = calendar.month_name[event_date.month] + f" {event_date.year}"

            # Ensure sheet exists
            ensure_month_sheet_exists(sheet, SPREADSHEET_ID, month_name)

            # Append event to proper sheet
            insert_event(sheet, SPREADSHEET_ID, month_name, event, total_hours)

# Schedule: run once daily at 20:00
schedule.every().day.at("20:00").do(process_work_events)


print("MCP Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(30)
