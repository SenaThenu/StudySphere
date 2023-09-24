"""
This stores all the reusable code snippets to use throughout the project.
"""

import requests
import typing

def get_row_ids(endpoint_url:str, headers:dict, database_id:str) -> tuple[int, list]:
    """
    ### Extracts the row IDs of a database.

    Args:
        endpoint_url (str): e.g. https://api.notion.com/v1
        headers (dict): Additional information to pass with the http request
        database_id (str): ID of the Database whose Row IDs are to be extracted

    Returns:
        int: Status code of the http request (e.g. 200-Success, 400-Failure)
        list: If successful, row_ids. Otherwise, error message!
    """
    # API endpoint to retrieve all pages (rows) in the database
    query_url = f"{endpoint_url}/databases/{database_id}/query"

    # Send a POST request to retrieve all pages
    query_response = requests.post(query_url, headers=headers)

    # Check if the request was successful
    if query_response.status_code == 200:
        data = query_response.json()
        # Extract row IDs from the query_response
        row_ids = [page["id"] for page in data["results"]]
        return query_response.status_code, row_ids
    else:
        return query_response.status_code, query_response.text

def extract_id_of_an_inline_databases(endpoint_url:str, headers:dict, parent_page_id:str) -> str:
    """
    ### Extracts the ID of an inline database within a given page ID.

    Args:
        endpoint_url (str): e.g. https://api.notion.com/v1
        headers (dict): Additional information to pass with the http request
        parent_page_id (str): ID of the page whose inline database ID should be extracted.

    Returns:
        str: The ID of the inline database
    """
    page_response = requests.get(f"{endpoint_url}/blocks/{parent_page_id}/children", headers=headers)
    response_json = page_response.json()
    children = response_json["results"]
    for child_block in children:
        if child_block["type"] == "child_database":
            return child_block["id"]

def get_page_title(endpoint_url:str, page_id:str, page_title_property_name:str = "Name") -> str:
    """
    ### Returns the title of a given page

    Args:
        endpoint_url (str): e.g. https://api.notion.com/v1
        headers (dict): Additional information to pass with the http request
        page_title_property_name (str, optional): The name of the column which contains page names. Defaults to "Name".

    Returns:
        str: The title of the page
    """

    page_response = requests.get(f"{endpoint_url}/pages/{page_id}")
    page_data = page_response.json()
    page_title = page_data["properties"][page_title_property_name]["title"][0]["text"]["content"]
    return page_title

def get_main_study_databases(endpoint_url, headers, parent_db_id:str) -> typing.Union[dict, None]:
    """
    ### Returns a dictionary with all the subjects in the main study database paired with their database ids.

    Args:
        endpoint_url (str): e.g. https://api.notion.com/v1
        headers (dict): Additional information to pass with the http request
        parent_db_id (str): The ID of the parent database which stores all the main subjects (e.g. StudySphere)

    Returns:
        dict: A dictionary with (key, value) pairs where key = subject_name and value = database_id 
        __OR__
        None: When an error occurs...
    """
    # Pair up the subject name to study database
    # Extracting page ids
    db_id_extraction_status, main_db_page_ids = get_row_ids(endpoint_url, headers, parent_db_id)
    if db_id_extraction_status != 200:
        print(f"An Error Occurred! \nError -> {main_db_page_ids}")  # When a failure occurs, main_db_page_ids contain the error message 
        return None
    else:
        pass

    main_study_databases = {} # Data is stored in (key, value) pairs where key = subject name, value = database id
    for page_id in main_db_page_ids:
        inline_db_id = extract_id_of_an_inline_databases(endpoint_url, headers, page_id)
        page_title = get_page_title(endpoint_url, page_id)
        main_study_databases[page_title] = inline_db_id
    return main_study_databases
