import os
from notion_client import Client

# Retrieve the token from an environment variable
notion_token = os.getenv("NOTION_TOKEN")
if notion_token is None:
    print("No token found. Please set the NOTION_TOKEN environment variable.")
else:
    print("Token found. Proceeding with initialization.")

# Initialize the Notion client with the token
notion = Client(auth=notion_token)

database_id = "2a8d1ec36f0e4608bf12eead3db39650"

try:
    # Fetch pages from the Notion database
    response = notion.databases.query(database_id=database_id)
    pages = response["results"]

    # Print the name of each page (event) found in the database
    for page in pages:
        # Check if the "Name" property and its title list are not empty
        if page["properties"].get("Name") and page["properties"]["Name"]["title"]:
            page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"Page Name: {page_name}")
        else:
            print("A page was found without a Name property or title.")


    # If pages are printed successfully, your authentication and query worked!
    print("Notion API authentication and database query successful!")

except Exception as e:
    # If an error occurs, print it out.
    print(f"An error occurred: {e}")