"""
Manages all the commands regarding setting up Spaced Repetition Dates in the Study Sphere.
"""
import requests
import json
import templates
from datetime import datetime, timedelta

def set_reps(endpoint_url: str, headers: dict, database_id: str, rep_intervals: list, date_format: str, page_title_property_name: str= "Lesson", rep_col_names: list= ["Rep 1", "Rep 2", "Rep 3"]):    
    # Extracting all the row ids of the database
    status, row_ids = templates.get_row_ids(endpoint_url, headers, database_id)
    if status != 200:
        print("An error occurred! Make sure the provided Database ID is valid!")
        return None
    else:
        pass
    
    # Selecting row_ids who don't have Rep Dates!
    valid_row_ids = []      # Stores all the rows which require repetition dates
    valid_row_names = []
    for row_id in row_ids:
        row_response = requests.get(f"{endpoint_url}/pages/{row_id}", headers=headers)
        row_data = row_response.json()
        if not row_data["properties"][rep_col_names[0]]["date"]:   # This becomes true if there's no date in the val_col
            valid_row_ids.append(row_id)
            valid_row_name = row_data["properties"][page_title_property_name]["title"][0]["text"]["content"]
            valid_row_names.append(valid_row_name)
        
    # Defining the current date
    now = datetime.now()
    
    for valid_row_i, valid_row_id in enumerate(valid_row_ids):
        # API endpoint for updating a property value in a row
        row_update_url = f"{endpoint_url}/pages/{valid_row_id}"

        # Specifying the update data
        data = {
            "properties": {}
        }

        for rep_i, rep_col_name in enumerate(rep_col_names):
            # To make this work, len(rep_col_names) must equal len(rep_intervals) and they should be corresponding
            data["properties"][rep_col_name] = {
                    "type": "date",
                    "date": {
                        "start": (now + timedelta(days=rep_intervals[rep_i])).strftime(date_format)
                    }
                }

        valid_row_response = requests.patch(row_update_url, json=data, headers=headers)

        # Check if the update was successful
        if valid_row_response.status_code == 200:
            print(f"Spaced Repetition Intervals were Successfully Added to {valid_row_names[valid_row_i]}!")
        else:
            print(f"An Error Occurred when Adding Repetition Dates to {valid_row_names[valid_row_i]}! :(")
    return None, None