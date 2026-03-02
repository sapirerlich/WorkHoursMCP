# DailyWorkHelper

**DailyWorkHelper** is an scheduled automation bot that scans your Google Calendar for "work" events and automatically logs them into a Google Sheet, calculating **total hours** for each event.

---

## Features

- Scans events containing the keyword `"work"` in your calendar  
- Inserts each event into Google Sheets with:  
  - Date  
  - Start time  
  - End time  
  - Total hours (numeric)  
- Runs automatically on a daily schedule  
- Fully autonomous agent simulation with dummy data for GitHub demo

---

## Setup & Run

1. Install required packages:

```bash
python3 -m venv venv                                           
source venv/bin/activate 
pip install --upgrade pip
pip install -r requirements.txt
python3 helper_main.py
