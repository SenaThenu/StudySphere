"""
This Python file connects all the bits of code to address user commands.
"""
import requests
import json
import rep_set

# Loading User Settings
with open("user_settings.json", "r") as f:
    user_settings = json.load(f)

# Necessary IDs
API_KEY = "secret_tIdRVQyO2kePasE4ACGSYnB3e99QUVCjz4mmp4eLWIc"
DATABASE_ID = "c47e37131ae7414bbfdde6337c73fab1"

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
REP_INTERVALS = user_settings["Rep-Intervals"]

rep_set.set_reps(END_POINT_URL, HEADERS, DATABASE_ID, REP_INTERVALS, DATE_FORMAT)