"""
Manages all the commands regarding setting up Spaced Repetition Dates in the Study Sphere.
"""
import requests
import json
from datetime import datetime, timedelta

def set_reps(endpoint_url, headers, database_id, rep_intervals, date_format):
    # API endpoint to retrieve all pages (rows) in the database
    query_url = f"{endpoint_url}/databases/{database_id}/query"

    # Send a POST request to retrieve all pages
    query_response = requests.post(query_url, headers=headers)

    # Check if the request was successful
    if query_response.status_code == 200:
        data = query_response.json()
        # Extract row IDs from the query_response
        row_ids = [page["id"] for page in data["results"]]
        print("Row IDs:", row_ids)
    else:
        return query_response.status_code, query_response.text
    
    # Defining the current date
    now = datetime.now()
    
    for row_id in row_ids:
        # API endpoint for updating a property value in a row
        row_update_url = f"{endpoint_url}/pages/{row_id}"

        # Specify the update data
        data = {
            "properties": {
                "Rep 1": {
                    "type": "date",
                    "date": {
                        "start": (now + timedelta(days=rep_intervals[0])).strftime(date_format)
                    }
                },
                "Rep 2": {
                    "type": "date",
                    "date": {
                        "start": (now + timedelta(days=rep_intervals[1])).strftime(date_format)
                    }
                },
                "Rep 3": {
                    "type": "date",
                    "date": {
                        "start": (now + timedelta(days=rep_intervals[2])).strftime(date_format)
                    }
                }
            }
        }

        row_response = requests.patch(row_update_url, json=data, headers=headers)

        # Check if the update was successful
        if row_response.status_code == 200:
            print("Spaced Repetition Intervals were Successfully Added!")
        else:
            print("An Error Occurred! :(")

