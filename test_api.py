import requests
import json

# Loading User Settings
with open("user_settings.json", "r") as f:
    user_settings = json.load(f)

# Necessary IDs
API_KEY = "secret_TGrfvNrdwP6DmQDpbUP9QAVZFF8e4e0N1B6XTauFUP1"
DATABASE_ID = "fb485f99d03940cebdd601f9cf38c057"

# Web Request Info
END_POINT_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Conventions
DATE_FORMAT = "%Y-%m-%d"

# Spaced-Repetition Variables
REP_INTERVALS = user_settings["Rep_Intervals"]

row_response = requests.get(f"{END_POINT_URL}/pages/{DATABASE_ID}", headers=HEADERS)
row_data = row_response.json()

with open("test.json", "w") as f:
    f.write(json.dumps(row_data))


print(row_data["properties"]["Revise Rep"]["date"])