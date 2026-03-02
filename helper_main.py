import schedule
import time as time_module
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from sheets_util import *

load_dotenv()

CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")
CALENDAR_ID = os.getenv("CALENDAR_ID")


calendar_service = get_calendar_service(CREDENTIALS_FILE)

sheet = get_sheet_service(CREDENTIALS_FILE)

def process_work_events():
    print("--------------------------------------------------")
    print("Starting work event processing...")
    
    try:
        print("Fetching events from Google Calendar...")
        events = get_today_events(calendar_service, CALENDAR_ID)
        print(f"Total events fetched: {len(events)}")

    except Exception as e:
        print("ERROR fetching calendar events:")
        print(e)
        return

    if not events:
        print("No events found for today.")
        return

    for event in events:
        title = event.get('summary', '')
        print(f"Checking event: '{title}'")

        if "work" not in title.lower():
            print("→ Skipping (not a work event)")
            continue

        print("→ Work event detected")

        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')

        if not start or not end:
            print("→ Skipping (missing start/end time)")
            continue

        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

            total_hours = (end_dt - start_dt).seconds / 3600
            event_date = start_dt.date().isoformat()
            month_name = start_dt.strftime("%B %Y")

            print(f"→ Date: {event_date}")
            print(f"→ Hours: {total_hours}")
            print(f"→ Target sheet: {month_name}")

            print("Ensuring month sheet exists...")
            ensure_month_sheet_exists(sheet, SPREADSHEET_ID, month_name)

            print("Inserting event into sheet...")
            if date_exists(sheet, SPREADSHEET_ID, month_name, event_date):
                print(f"→ Skipping {event_date}, already added")
            else:
                insert_event(
                    sheet,
                    SPREADSHEET_ID,
                    month_name,
                    {
                        "date": event_date,
                        "start": start_dt.strftime("%H:%M"),
                        "end": end_dt.strftime("%H:%M")
                    },
                    total_hours
                )
                print(f"✓ Successfully inserted {event_date}")

        except Exception as e:
            print("ERROR processing event:")
            print(e)

    print("Finished processing events.")
    print("--------------------------------------------------")

# Schedule: run once daily at 20:00
schedule.every().day.at("12:50").do(process_work_events)


print("Work Hours Bot started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time_module.sleep(30)
