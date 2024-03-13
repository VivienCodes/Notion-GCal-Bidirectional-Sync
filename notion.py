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
            page_name = "Unamed Page"
            print("A page was found without a Name property or title.")

        # Safely access "Date" property
        if page["properties"].get("Date") and page["properties"]["Date"]["date"]:
            if page["properties"]["Date"]["date"]["start"]:
                start_date = page["properties"]["Date"]["date"]["start"]
                # Optional: Parse and format the start date for readability
                try:
                    # For dates including times, adjust the parsing format as needed
                    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except ValueError:
                    # Fallback for dates that include time or if parsing fails
                    formatted_date = start_date
            else:
                formatted_date = "No Start Date"
        else:
            formatted_date = "No Date Property Found"
        print(f"Page Name: {page_name}, Start Date: {formatted_date}")    
    # If pages are printed successfully, your authentication and query worked!
    print("Notion API authentication and database query successful!")

except Exception as e:
    # If an error occurs, print it out.
    print(f"An error occurred: {e}")