from datetime import datetime
from sheets_util import *
from config import * 

def process_work_events(calendar_service, sheet, calendar_id, spreadsheet_id):
    print("--------------------------------------------------")
    print("Starting work event processing...")
    
    try:
        print("Fetching events from Google Calendar...")
        events = get_today_events(calendar_service, calendar_id)
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
            ensure_month_sheet_exists(sheet, spreadsheet_id, month_name)

            print("Inserting event into sheet...")
            if date_exists(sheet, spreadsheet_id, month_name, event_date):
                print(f"→ Skipping {event_date}, already added")
            else:
                insert_event(
                    sheet,
                    spreadsheet_id,
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

def main():
    config = load_config()
    calendar_id = config['calendar_id']
    spreadsheet_id = config['spreadsheet_id']
    calendar_service = get_calendar_service(config['creds'])
    sheet = get_sheet_service(config['creds'])
    process_work_events(calendar_service, sheet, calendar_id, spreadsheet_id)

if __name__ == "__main__":
    print("Work Hours Bot started")
    main()