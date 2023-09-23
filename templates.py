"""
This stores all the reusable code snippets to use throughout the project.
"""

import requests, json

# Replace with your Notion API token and page ID
token = "secret_tIdRVQyO2kePasE4ACGSYnB3e99QUVCjz4mmp4eLWIc"
page_id = "27b7a993eca54350b4c70e99f6315f0d"

# Create headers with the API token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  # Specify the Notion API version here
}

# Get the block children from the Notion page
url = f"https://api.notion.com/v1/blocks/{page_id}/children"
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract the block data from the response
    blocks = data["results"]
    with open("test.json", "w") as f:
        f.write(json.dumps(blocks))
else:
    print(f"Failed to retrieve data from Notion API. {response.status_code} - {response.text}")

