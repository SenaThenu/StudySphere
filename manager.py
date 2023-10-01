"""
This Python file connects all the bits of code to address user commands.
"""

from termcolor import colored, cprint  # To add terminal colours
from pyfiglet import figlet_format  # To generate ASCII art (Header!)

import requests
import json
import time
from datetime import datetime, timedelta

import templates

def load_global_settings():
    """This is a special function which is used to update the global settings from user_settings.json"""
    # Loading User Settings
    with open("user_settings.json", "r") as f:
        user_settings = json.load(f)
        f.close()
        # In each setting in the json file, index 0 stores the description of the setting while index 1 holds the real value!

    global API_KEY, STUDY_SPHERE_ID, END_POINT_URL, HEADERS, REP_INTERVALS, INSTRUCTIONS
    
    # Necessary IDs
    API_KEY = user_settings["API_KEY"][1]
    STUDY_SPHERE_ID = user_settings["StudySphere_ID"][1]

    # Web Request Info
    END_POINT_URL = "https://api.notion.com/v1"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Displaying Instructions
    INSTRUCTIONS = user_settings["Instructions"][1]

    # Spaced-Repetition Variables
    REP_INTERVALS = user_settings["Rep_Intervals"][1] # A list of repetition intervals whose values are in days!

# Loading global variables from user_settings
load_global_settings()

# Conventions
DATE_FORMAT = "%Y-%m-%d"

# --- Start Creating the CLI ---

# Specifying Common CMDs
YES_CMDS = ["y", "yes", "yep", "yeah", "1"]
NO_CMDS = ["n", "no", "nope", "nah", "0"]
HELP_CMDS = ["h", "help"]
EXIT_CMDS = ["e", "exit", "q", "quit", "c", "close"]
INCLUDE_ALL = ["*", "."]
INCLUDE_NONE = ["", "n"]
SETTINGS_CMDS = ["s", "setting", "settings"]
SET_REP_CMDS = ["set-rep", "set-reps", "set-repetitions", "set repetitions"]
SET_REVISION_CMDS = ["set-rev", "set-revs", "set-revision"]

# Some colour variables (Use these to add terminal colours only in special occasions, e.g. printing doc-strings! Otherwise, use termcolor)
# Define global color variables
HEADER_COLOR = "\033[1m\033[94m"  # Bold and light blue
RESET_COLOR = "\033[0m"  # Reset to default color
CMD_COLOR = "\033[92m"  # Light green
NOTE_COLOR = "\033[93m"  # Light yellow
EMOJI_COLOR = "\033[94m"  # Light blue


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

def get_user_input(prompt: str, exit_message: str, help_message: str, validate: bool=True, is_int: bool=False, options:list=[], match_length: bool=False) -> str:
    """
    ### Returns the user's response for the given prompt. Includes validation functionality!

    Args:
        prompt (str): What to ask from the user to get the input!
        exit_message (str): The message to display in case the user asks to leave!
        help_message (str): Message to display if the user requires help!
        validate (bool, optional): Whether the user input should be validated before returning. Defaults to True.
        * below are validation parameters *
        is_int (bool, optional): Validates if the user_input should be an integer!
        options (list, optional): Options refer to the possible answers for the prompt. If match length is False, returns the user input if it is present in the options!
        match_length (bool, optional): Whether the validation should be done through matching the length of an option or the user input. Defaults to False.

    Returns:
        str: The validated user input!
    """
    valid_input = False
    while not valid_input:
        user_input = input(prompt).strip()
        if not validate:
            break
        elif options:
            if user_input in options and not match_length:
                valid_input = True
            elif match_length and len(user_input) == len(options[0]):
                valid_input = True
        elif user_input in EXIT_CMDS:
            valid_input = True
            print(exit_message)
            time.sleep(3)
            quit()
        elif user_input in HELP_CMDS:
            print(help_message)
            continue
        elif is_int:
            try:
                validated_input = int(user_input)
                return validated_input
            except:
                print(colored("Hey, you are supposed to type out a number🤨!", "red"))
                continue
        else:
            print(colored("Oops! 😕 I don't recognize it!", "red"))
            continue
    return user_input

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
    elif current_command in INCLUDE_NONE:
        return {}
    elif current_command[:2] == "ex":
        try:
            exclude_branch_nums = current_command[2:].split(",")
            exclude_branch_nums = [int(i) for i in exclude_branch_nums]
        except:
            print(colored("Please make sure the exclusion list is correct!", "red"))
            print(colored("If you feel stuck, ask for help (h)!", "yellow"))
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
            print(colored("Please make sure the inclusion list is correct!", "red"))
            print(colored("If you feel stuck, just type 'h' for help!", "yellow"))
            return get_valid_dict_data(raw_dict, exit_message, help_message)

        valid_dict = {}
        for include_branch_num in include_branch_nums:
            # Transferring to-be-included data to a new dictionary.
            valid_dict[list(raw_dict.keys())[include_branch_num-1]] = raw_dict[list(raw_dict.keys())[include_branch_num-1]]
        return valid_dict

def set_reps_for_pages(database_id: str, is_revision_rep:bool=False, revision_date:str=None, page_title_property_name: str= "Lesson", rep_col_names: list= ["Rep 1", "Rep 2", "Rep 3"], revision_col_name:str= "Revise Rep"):
    """
    ### Adds spaced repetition intervals or revision reps to pages in a given Database!

    Args:
        database_id (str): ID of the database
        is_revision_rep (bool, optional): Whether the function should add revision reps (True) or spaced/normal reps (False). Defaults to False.
        revision_date (str, required if is_revision_rep=False): The date revision should be added to.
        page_title_property_name (str, optional): The title of the primary column of the database. Defaults to "Lesson".
        rep_col_names (list, optional): The title of the spaced repetition columns in the database. Defaults to ["Rep 1", "Rep 2", "Rep 3"].
        revision_col_name (str, optional): The name of the revision column in the database. Defaults to "Revision Rep".

    Returns:
        Nothing!
    """
    # Extracting all the row ids of the database. In fact, row_ids are the database ids of the dbs in the parent db's
    status, row_ids = templates.get_row_ids(END_POINT_URL, HEADERS, database_id)
    if status != 200:
        print(colored("❌ An error occurred! Make sure the provided Database ID is valid!", "red"))
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
            if is_revision_rep:
                row_data["properties"][revision_col_name]["date"] # This errors if there's no revision column
                _append_row_id_and_name(row_id, row_data, valid_row_ids, valid_row_names, page_title_property_name)
            else:
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

        if is_revision_rep:
            data["properties"][revision_col_name] = {
                "type": "date",
                "date": {
                    "start": revision_date
                }
            }
        else:
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
            print(colored(f"    ✅ Revision was successfully set to {valid_row_names[valid_row_i]}!", "green")) if is_revision_rep else print(colored(f"    ✅ Spaced Repetition Intervals were successfully set to {valid_row_names[valid_row_i]}!", "green"))
        else:
            print(colored(f"    ❌ Error: Revision could not be set to {valid_row_names[valid_row_i]}!", "red")) if is_revision_rep else print(colored(f"    ❌ Error: Spaced Repetition Intervals could not be added to {valid_row_names[valid_row_i]}!", "red"))

    # Dealing with sub_branched_rows
    if sub_branched_row_names:
        try:
            sub_branch_dict = {}
            for sub_branch_i, sub_branch_name in enumerate(sub_branched_row_names):
                sub_branch_dict[sub_branch_name] = templates.extract_id_of_an_inline_databases(END_POINT_URL, HEADERS, sub_branched_row_ids[sub_branch_i])
            print(colored("✨ Apparently, this seems to have sub-branches! I have listed them below...", "green"))
            set_bulk_reps(sub_branch_dict, is_revision_rep, revision_date)
        except:
            print(colored("Skipped because of an error!", "red"))

def set_bulk_reps(branches_dict:dict, revision_rep:bool=False, global_revision_date:str=None):
    """
    ### Sets up repetitions for every branch given in the branches_dict.

    Args:
        branches_dict (dict): A dictionary of branches with key being the branch_name and the value being the branch_id
        revision_rep (bool): Whether reps are for revision (True) or not (False)
    """
    for i, branch in enumerate(branches_dict):
        print(colored(f"    {i+1}. {branch}", "blue", attrs=["bold"]))
        # Because of i+1 we are taking indices starting from 1...
    current_help_message = colored("If you want to include only specific branches, enter branch numbers separated by commas. e.g. 1,2,3\nIn case you wanna exclude those branches, add `ex`: e.g. ex1,2,3\nIf you want to add repetitions for\n    - all branches, type *\n    - none of branches, leave blank\nIf any of the above branches have sub-branches in them, don't worry, I'll inform you and get your instructions! :)", "cyan")
    if INSTRUCTIONS:
        print(current_help_message)
    
    branches_to_add_reps = get_valid_dict_data(branches_dict, exit_message=colored("😭 Oops! Sad to see you leaving while setting up repetition dates.", "red"), help_message=current_help_message)
    # The above code blocks segregates all the branches that need repetition dates to be added!

    for branch in branches_to_add_reps:
        branch_id = branches_to_add_reps[branch]
        
        if revision_rep:
            print(colored(f"🚀 Started Setting Revision to {branch}!", "blue"))
            if global_revision_date:
                revision_date = global_revision_date
            else:
                revision_date = get_user_input(colored(f"📅 Enter the revision date for {branch} (YYYY-MM-DD): ", "blue"), colored(f"😭 Sad to see you leaving while adding a Revision Date for {branch}!", "red"), colored("Just enter the date in the format YYYY-MM-DD! (e.g. 2077-05-09)", "magenta"), options=["YYYY-MM-DD"], match_length=True)
            set_reps_for_pages(branch_id, is_revision_rep=True, revision_date=revision_date)
            print(colored(f"Ended Setting Revision to {branch}!", "blue"))
        else:
            print(colored(f"🚀 Started Adding Repetitions to {branch}!", "blue"))
            set_reps_for_pages(branch_id)
            print(colored(f"✅ Ended Adding Repetitions to {branch}!", "blue"))

def main():
    # Welcome Header
    cprint(figlet_format("StudySphere Manager!", "doom"), "green", attrs=["bold"])

    # Command Lists
    program_alive = True
    while program_alive:
        command = get_command(colored("> ", "green"))
        if bulk_match_user_response(command, HELP_CMDS):
            # Checks whether user asks for help
            print(f"""
                {CMD_COLOR}Supported Commands:{RESET_COLOR}
                {CMD_COLOR}
                {EMOJI_COLOR}📅 set-rep{RESET_COLOR} -> Sets up repetition dates for notes when the first repetition date column is empty.
                {EMOJI_COLOR}🔄 set-revision{RESET_COLOR} -> Sets up revision dates for notes.
                {EMOJI_COLOR}🔧 settings{RESET_COLOR} -> Enables you to change settings!
                {EMOJI_COLOR}💨 exit (e){RESET_COLOR} -> Exits the program.

                {NOTE_COLOR}Note:{RESET_COLOR} You can specify which notes along the way...
            """)
        elif bulk_match_user_response(command, EXIT_CMDS):
            # Checks whether user asks to leave
            print(colored("🍀 Hope you fulfilled your purposes! Good Luck with Studying! 🚀", "green", attrs=["bold"]))
            time.sleep(3)
            program_alive = False
        elif bulk_match_user_response(command, SET_REP_CMDS):
            main_branches_dict = templates.get_child_databases(END_POINT_URL, HEADERS, STUDY_SPHERE_ID)
            if main_branches_dict:  # Checks whether the API request has been successful
                print(colored("Gotcha! I can add repetitions for the following StudySphere branches!", "green"))
                set_bulk_reps(main_branches_dict)
            else:
                # If the API request failed, the user has already seen an error message!
                print(colored("Error: Please make sure the Database ID of the StudySphere is correct! 🔍", "red"))
                continue
        elif bulk_match_user_response(command, SET_REVISION_CMDS):
            print(colored("Alright! Choose an option below😉:", "cyan"))
            print(colored("   Option 1: Set different revision repetition dates for each branch.", "yellow"))
            print(colored("   Option 2: Set the same revision repetition date for selected branches.", "yellow"))
            
            option = get_user_input(colored("Enter only the option number😁: ", "cyan"), colored("😭 Sad to see you leave in the middle of setting repetition dates!", "red"), colored("What do you prefer, option 1 or 2?", "magenta"), options=["1", "2"])
            print(colored(f"Yay, you selected option {option}! 🎉", "green"))
            main_branches_dict = templates.get_child_databases(END_POINT_URL, HEADERS, STUDY_SPHERE_ID)

            if main_branches_dict:
                print(colored("📅 I can set revision dates for the following branches!", "blue"))
            else:
                print(colored("🥲 Please make sure the Database ID of the StudySphere is correct!", "red", attrs=["bold"]))
                continue
            # By this point, the option can only be 1 or 2...
            if option == "1":
                set_bulk_reps(main_branches_dict, True)
            else:
                revision_date = get_user_input(colored("Before I show you those cool branches, please enter your desired revision date (YYYY-MM-DD): ", "blue"), colored("😭 Sad to see you leave in the middle of setting up revision dates!", "red"), colored("Just enter the date in the format YYYY-MM-DD! (e.g. 2077-05-09)"), options=["YYYY-MM-DD"], match_length=True)
                set_bulk_reps(main_branches_dict, True, revision_date)
        elif bulk_match_user_response(command, SETTINGS_CMDS):
            all_settings_modified = False
            
            while not all_settings_modified:
                with open("user_settings.json", "r") as read_settings:
                    user_settings = json.load(read_settings)
                    read_settings.close()

                print(colored("I can modify the following settings ⚙️!", "green", attrs=["bold"]))

                for i, setting in enumerate(user_settings):
                    print(colored(f"    {i+1}. {setting} - {user_settings[setting][0]}", "blue"))
                    print(colored(f"        This is currently set to {user_settings[setting][1]}", "magenta"))
                    if setting == "Instructions":
                        print(colored("No need to deal with the following settings (apart from Rep_Intervals) as long as you don't modify the columns in the StudySphere template!", "blue", attrs=["bold"]))
                    elif setting == "Rep_Col_Names":
                        print(colored("         ❗Important: the length of Rep_Col_Names must be equal to the length of Rep_Intervals", "red"))
                # This is specified to segregate settings which require lists because the program can't directly accept lists
                list_settings = [setting_name for setting_name in user_settings if type(user_settings[setting_name][1]) == list]

                # The setting number
                setting_i_to_modify = get_user_input(colored("Enter only the setting number to modify it: ", "cyan"), colored("😭 Sad to see you leaving in the middle of modifying settings!", "red"), colored("No worries! Just refer to the official documentation: ", "yellow"), is_int=True)
                # setting_i_to_modify indices start from 1.
                setting_to_modify = list(user_settings.keys())[setting_i_to_modify-1]

                if setting_i_to_modify > 0 and setting_i_to_modify <= len(user_settings):
                    if setting_to_modify in list_settings:
                        new_list = []
                        elements_are_int = type(user_settings[setting_to_modify][1][0]) == int

                        # Iteratively asking each element in the list from the user
                        n_elements = get_user_input(colored(f"We need a list to update {setting_to_modify}\nSo, enter the number of elements in the new list: ", "yellow"), colored("😭 Sad to see you leave while thinking about the number of elements in a list...", "red"), colored("Just tell me how many values are in the new list you wanna set this setting to!", "yellow"), is_int=True)
                        
                        for element_i in range(n_elements):
                            new_element = get_user_input(colored(f"Enter element number {element_i+1}: ", "yellow"), colored("😭 Sad to see you leave while specifying your fancy list!", "red"), colored("Just type what you want your list to have at this position!", "yellow"), is_int=elements_are_int)
                            new_list.append(new_element)

                        # Updating the user_settings
                        user_settings[setting_to_modify][1] = new_list
                        print(colored("🎉 Yay, the setting has been successfully configured!", "green", attrs=["bold"]))
                    else:
                        new_setting = get_user_input(colored(f"Enter the value you wanna set to {setting_to_modify}: ", "yellow"), colored(f"😭 Sad to see you leave while modifying the setting {setting_to_modify}", "red"), colored(f"Oh! Just enter the new value you set to {setting_to_modify}!", "yellow"), validate=False)
                        user_settings[setting_to_modify][1] = new_setting
                    
                    with open("user_settings.json", "w") as new_user_settings:
                        json.dump(user_settings, new_user_settings)
                        new_user_settings.close()
                    print(colored(f"Successfully updated -> {setting_to_modify}🎉!", "green"))

                    another_round = get_user_input(colored("Do you want to modify another setting? (y/n): ", "cyan"), colored("Hope the new setting fulfills your purposes! All the best!😍", "green", attrs=["bold"]), colored("Just type y for yes and n for no!", "yellow"), options=YES_CMDS+NO_CMDS)
                    if bulk_match_user_response(another_round, YES_CMDS):
                        continue
                    else:
                        print("Alright! Feel free to modify any other setting later...")
                        break
                else:
                    print(colored("🤭 Oops! That's an invalid setting number!", "red"))
                    continue
            
            # To load the new settings
            load_global_settings()
        else:
            print(colored("🥺 Oops, I don't recognize that command!", "red"))
    quit()

main()