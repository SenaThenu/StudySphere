"""
This Python file connects all the bits of code to address user commands.
"""
import requests
import json
import time

import rep_set
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
REP_INTERVALS = user_settings["Rep_Intervals"]
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
        except:
            print("Please make sure the inclusion list is correct!\nIf you feel stuck, ask for help(h)!")
            return get_valid_dict_data(raw_dict, exit_message, help_message)

        valid_dict = {}
        for include_branch_num in include_branch_nums:
            # Transferring to-be-included data to a new dictionary.
            valid_dict[list(raw_dict.keys())[include_branch_num-1]] = raw_dict[list(raw_dict.keys())[include_branch_num-1]]
        return valid_dict

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
            main_branches_dict = templates.get_main_branch_databases(END_POINT_URL, HEADERS, STUDY_SPHERE_ID)

            if main_branches_dict:  # Checks whether the API request has been successful
                print("Gotcha! I can add repetitions for the following StudySphere branches!")
                for i, branch in enumerate(main_branches_dict):
                    print(f"{i+1}. {branch}")
                    # Because of i+1 we are taking indices starting from 1...
                current_help_message = "If you want to include only specific branches, enter branch numbers separated by commas. e.g. 1,2,3\nIn case you wanna exclude those branches, add `ex`: e.g. ex1,2,3\nIf you want to add repetitions for all branches leave blank!"
                if INSTRUCTIONS:
                    print(current_help_message)
                
                branches_to_add_reps = get_valid_dict_data(main_branches_dict, exit_message=":( Sad to see you leave in the middle of setting Spaced Repetitions!", help_message=current_help_message)
                # The above code blocks segregates all the branches that need repetition dates to be added!
                
                for branch in branches_to_add_reps:
                    branch_id = branches_to_add_reps[branch]
                    print(f"Started Adding Repetitions to {branch}")
                    rep_set.set_reps(END_POINT_URL, HEADERS, branch_id, REP_INTERVALS, DATE_FORMAT)
                    print(f"Ended Adding Repetitions to {branch}")
            else:
                # If the API request failed, the user has already seen an error message!
                print("Please make sure the Database ID of the StudySphere is correct!")
                continue
        else:
            print("Oops, I don't recognize that command!")
    quit()

main()