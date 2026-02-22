import schedule
import time
from datetime import datetime

# Dummy Google Sheets function
def insert_into_sheet(event):
    print(f"Inserting into Sheet: {event['date']} | {event['start']}-{event['end']} | {event['title']}")

# MCP logic
def process_work_events():
    print("Checking for work events...")
    for event in dummy_events:
        if "עבודה" in event['title']:
            insert_into_sheet(event)

# Scheduler: run once a day at 18:00
schedule.every().day.at("18:00").do(process_work_events)

print("MCP Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(30)
