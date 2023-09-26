"""
This Python file connects all the bits of code to address user commands.
"""
import requests
import json
import time
from datetime import datetime, timedelta

import templates

# Loading User Settings
with open("user_settings.json", "r") as f:
    user_settings = json.load(f)

# Necessary IDs
API_KEY = "secret_TGrfvNrdwP6DmQDpbUP9QAVZFF8e4e0N1B6XTauFUP1"
STUDY_SPHERE_ID = user_settings["StudySphere_ID"]

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
REP_INTERVALS = user_settings["Rep_Intervals"] # A list of repetition intervals whose values are in days!
INSTRUCTIONS = user_settings["Instructions"]

# --- Start Creating the CLI ---

# Specifying Common CMDs
HELP_CMDS = ["h", "help"]
EXIT_CMDS = ["e", "exit", "q", "quit", "c", "close"]
INCLUDE_ALL = ["", "*", "."]

def get_command(prompt:str) -> str:
    """
    ### Gets the user command + does all the necessary formatting!

    Args:
        prompt (str): What to be asked from the user...

    Returns:
        str: The user's answer
    """
    command = input(f"{prompt} ").lower().strip()
    return command

def bulk_match_user_response(user_command:str, valid_commands:list) -> bool:
    """
    ### Checks whether the user's command is in the valid_commands.

    Args:
        user_command (str)
        valid_commands (list)

    Returns:
        bool: Whether the user's command is in valid_commands (True) or not (False)
    """
    if user_command in valid_commands:
        return True
    else:
        return False

def get_valid_dict_data(raw_dict:dict, exit_message:str, help_message:str) -> dict:
    """
    ### Takes in a raw_dictionary and filters out the data required by the user! (i.e. either includes or excludes!)
    Here, the program assumes the list of indices user enters start from 1.

    Args:
        raw_dict (dict): The Raw Dictionary
        exit_message (str): The message to display when the user asks to exit
        help_message (str): The message to display when the user asks for help

    Returns:
        dict: The data user wants
    """
    current_command = get_command("> ")

    if current_command in INCLUDE_ALL:
        return raw_dict
    elif current_command[:2] == "ex":
        try:
            exclude_branch_nums = current_command[2:].split(",")
            exclude_branch_nums = [int(i) for i in exclude_branch_nums]
        except:
            print("Please make sure the exclusion list is correct!\nIf you feel stuck, ask for help(h)!")
            return get_valid_dict_data(raw_dict, exit_message, help_message)
        
        for exclude_branch_num in exclude_branch_nums:
            # Deleting the unnecessary branches
            raw_dict.pop(list(raw_dict.keys())[exclude_branch_num-1])
        return raw_dict
    elif bulk_match_user_response(current_command, HELP_CMDS):
        print(help_message)
        return get_valid_dict_data(raw_dict, exit_message, help_message)
    elif bulk_match_user_response(current_command, EXIT_CMDS):
        # Checks whether the user wants to exit!
        print(exit_message)
        time.sleep(3)
        quit()
    else:
        try:
            include_branch_nums = current_command.split(",")
            include_branch_nums = [int(i) for i in include_branch_nums]
        except:
            print("Please make sure the inclusion list is correct!\nIf you feel stuck, ask for help(h)!")
            return get_valid_dict_data(raw_dict, exit_message, help_message)

        valid_dict = {}
        for include_branch_num in include_branch_nums:
            # Transferring to-be-included data to a new dictionary.
            valid_dict[list(raw_dict.keys())[include_branch_num-1]] = raw_dict[list(raw_dict.keys())[include_branch_num-1]]
        return valid_dict

def set_reps_for_pages(database_id: str, page_title_property_name: str= "Lesson", rep_col_names: list= ["Rep 1", "Rep 2", "Rep 3"]):
    """
    ### Adds spaced repetition intervals to pages in a given Database!

    Args:
        database_id (str): ID of the database
        page_title_property_name (str, optional): The title of the primary column of the database. Defaults to "Lesson".
        rep_col_names (list, optional): The title of the spaced repetition columns in the database. Defaults to ["Rep 1", "Rep 2", "Rep 3"].

    Returns:
        Nothing!
    """
    # Extracting all the row ids of the database. In fact, row_ids are the database ids of the dbs in the parent db's
    status, row_ids = templates.get_row_ids(END_POINT_URL, HEADERS, database_id)
    if status != 200:
        print("An error occurred! Make sure the provided Database ID is valid!")
        return None   # This return has been used to break the function!
    else:
        pass
    
    def _append_row_id_and_name(row_id, row_data, id_list, name_list, name_col="Name"):
        # This is private to this function!
        id_list.append(row_id)
        row_name = row_data["properties"][name_col]["title"][0]["text"]["content"]
        name_list.append(row_name)

    # Selecting row_ids which don't have Rep Dates!
    valid_row_ids = []      # Stores all the rows which require repetition dates
    valid_row_names = []
    sub_branched_row_ids = []
    sub_branched_row_names = []
    for row_id in row_ids:
        row_response = requests.get(f"{END_POINT_URL}/pages/{row_id}", headers=HEADERS)
        row_data = row_response.json()
        try:
            if not row_data["properties"][rep_col_names[0]]["date"]:   # This becomes true if there's no date in the val_col
                _append_row_id_and_name(row_id, row_data, valid_row_ids, valid_row_names, page_title_property_name)
        except:
            # This is triggered when the database within the page doesn't contain repetition columns.
            # According to the official StudySphere template, such databases can be branched subjects!
            _append_row_id_and_name(row_id, row_data, sub_branched_row_ids, sub_branched_row_names)
            
    # Defining the current date
    now = datetime.now()
    
    # Dealing with valid row_ids (normal)
    for valid_row_i, valid_row_id in enumerate(valid_row_ids):
        # API endpoint for updating a property value in a row
        row_update_url = f"{END_POINT_URL}/pages/{valid_row_id}"

        # Specifying the update data
        data = {
            "properties": {}
        }

        for rep_i, rep_col_name in enumerate(rep_col_names):
            # To make this work, len(rep_col_names) must equal len(REP_INTERVALS) and they should be corresponding
            data["properties"][rep_col_name] = {
                    "type": "date",
                    "date": {
                        "start": (now + timedelta(days=REP_INTERVALS[rep_i])).strftime(DATE_FORMAT)
                    }
                }

        valid_row_response = requests.patch(row_update_url, json=data, headers=HEADERS)

        # Check if the update was successful
        if valid_row_response.status_code == 200:
            print(f"Spaced Repetition Intervals were Successfully Added to {valid_row_names[valid_row_i]}!")
        else:
            print(f"An Error Occurred when Adding Repetition Dates to {valid_row_names[valid_row_i]}! :(")

    # Dealing with sub_branched_rows
    if sub_branched_row_names:
        try:
            sub_branch_dict = {}
            for sub_branch_i, sub_branch_name in enumerate(sub_branched_row_names):
                sub_branch_dict[sub_branch_name] = templates.extract_id_of_an_inline_databases(END_POINT_URL, HEADERS, sub_branched_row_ids[sub_branch_i])
            print("Apparently, this seems to have sub-branches! I have listed them below...")
            set_bulk_reps(sub_branch_dict)
        except:
            print("Skipped because of an error!")

def set_bulk_reps(branches_dict:dict):
    """
    ### Sets up repetitions for every branch given in the branches_dict.

    Args:
        branches_dict (dict): A dictionary of branches with key being the branch_name and the value being the branch_id
    """
    for i, branch in enumerate(branches_dict):
        print(f"{i+1}. {branch}")
        # Because of i+1 we are taking indices starting from 1...
    current_help_message = "If you want to include only specific branches, enter branch numbers separated by commas. e.g. 1,2,3\nIn case you wanna exclude those branches, add `ex`: e.g. ex1,2,3\nIf you want to add repetitions for all branches leave blank!\nIf any of the above branches have sub-branches in them, don't worry, I'll take care of them with your instructions! :)"
    if INSTRUCTIONS:
        print(current_help_message)
    
    branches_to_add_reps = get_valid_dict_data(branches_dict, exit_message=":( Sad to see you leave in the middle of setting Spaced Repetitions!", help_message=current_help_message)
    # The above code blocks segregates all the branches that need repetition dates to be added!

    for branch in branches_to_add_reps:
        branch_id = branches_to_add_reps[branch]
        print(f"Started Adding Repetitions to {branch}")
        set_reps_for_pages(branch_id)
        print(f"Ended Adding Repetitions to {branch}")

def main():
    # Command Lists
    program_alive = True
    while program_alive:
        command = get_command("> ")
        if bulk_match_user_response(command, HELP_CMDS):
            # Checks whether user asks for help
            print("""
                Supported Commands:
                    * set-rep -> Sets up repetition dates for notes when first repetition date column is empty!
                    * exit (e) -> Exits the program
                Note: You can specify which notes along the way...
            """)
        elif bulk_match_user_response(command, EXIT_CMDS):
            # Checks whether user asks to leave
            print("Hope you fulfilled your purposes! Good Luck \w Studying!")
            time.sleep(3)
            program_alive = False
        elif command == "set-rep":
            main_branches_dict = templates.get_child_databases(END_POINT_URL, HEADERS, STUDY_SPHERE_ID)
            if main_branches_dict:  # Checks whether the API request has been successful
                print("Gotcha! I can add repetitions for the following StudySphere branches!")
                set_bulk_reps(main_branches_dict)
            else:
                # If the API request failed, the user has already seen an error message!
                print("Please make sure the Database ID of the StudySphere is correct!")
                continue
        else:
            print("Oops, I don't recognize that command!")
    quit()

main()