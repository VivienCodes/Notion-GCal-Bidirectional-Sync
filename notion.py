import os
from notion_client import Client
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Notion Setup
notion_token = os.getenv("NOTION_TOKEN")
notion = Client(auth=notion_token)
database_id = "2a8d1ec36f0e4608bf12eead3db39650"

# Google Calendar Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=creds)

# Function to create an event in Google Calendar
def create_event(service, summary, start_datetime):
    event_start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d").isoformat() + "+10:00"  # Assuming the event starts at 00:00 Sydney time
    event_end_datetime = (datetime.strptime(start_datetime, "%Y-%m-%d") + timedelta(days=1)).isoformat() + "+10:00"  # Next day, same time for end
    
    event = {
        'summary': summary,
        'start': {
            'dateTime': event_start_datetime,
            'timeZone': 'Australia/Sydney',
        },
        'end': {
            'dateTime': event_end_datetime,
            'timeZone': 'Australia/Sydney',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created event {created_event['summary']} on {created_event['start']['dateTime']}")

try:
    # Fetch pages from the Notion database
    response = notion.databases.query(database_id=database_id)
    pages = response["results"]

    for page in pages:
        if page["properties"].get("Name") and page["properties"]["Name"]["title"]:
            page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            if page["properties"].get("Date") and page["properties"]["Date"]["date"]:
                page_date = page["properties"]["Date"]["date"]["start"]
                # Call the function to create an event in Google Calendar for each Notion page
                create_event(service, page_name, page_date)

except Exception as e:
    print(f"An error occurred: {e}")