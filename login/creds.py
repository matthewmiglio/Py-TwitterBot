import PySimpleGUI as sg
import os


# method to get appdata directory
def get_appdata_directory():
    """method to get appdata directory

    Args:
        None

    Returns:
        string: the appdata directory

    """

    return os.getenv("APPDATA")


# method to make the creds.txt file at appdata/roaming/Py-TwitterBot\creds.txt
def make_creds_file():
    """method to make the creds.txt file at appdata/roaming/Py-TwitterBot\creds.txt

    Args:
        None

    Returns:
        None

    """

    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    with open(directory, "w") as f:
        f.write('Username: ""' + "\n")
        f.write('Password: ""')
    print(f"Made creds file @ {directory}")


# method to check if creds.txt exists in appdata/roaming/Py-TwitterBot
def check_if_creds_file_exists():
    """method to check if creds.txt exists in appdata/roaming/Py-TwitterBot

    Args:
        None

    Returns:
        boolean: True if creds.txt exists, False if it does not

    """

    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    return os.path.exists(directory)


# method to get creds from creds.txt
def get_creds_from_file():
    """method to get the twitter login credentials stored in creds.txt in the py-twitterbot directory

    Args:
        None

    Returns:
        string, string: the username , password

    """
    user = ""
    password = ""

    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    with open(directory, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Username:"):
                user = parse_cred_line(line[9:])
            if line.startswith("Password:"):
                password = parse_cred_line(line[9:])

    return user, password


# method to parse cred line from creds.txt file
def parse_cred_line(line):
    """method to parse the credential line in the creds.txt file

    Args:
        line: the line to parse

    Returns:
        string: the parsed line

    """
    new_line = ""
    for char in line:
        if char == " " or char == "\n" or char == '"':
            continue
        new_line = new_line + char
    return new_line


# method to popup a gui when user is missing crds in creds.txt
def show_missing_creds_in_auth_file_gui(location):
    """method to show a gui to the user alerting the mof missing creds in the creds.txt file

    Args:
        location: the location of the creds.txt file

    Returns:
        None

    """
    out_text = (
        "TWITTER LOGIN CREDENTIALS MISSING IN creds.txt!\n\n"
        + f"Please write in your Twitter login in the file at [{location}] in the format outlined in the new file.\n"
        + "Restart the program after these changes..."
    )
    sg.theme("SystemDefaultForReal")
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("CRITICAL ERROR- User Action Required", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()


# method to check if the creds.txt file is empty or not
def check_if_creds_file_is_empty():
    """method to check if the creds.txt file is empty

    Args:
        None

    Returns:
        boolean: True if the file is empty, False if it is not empty

    """
    creds = get_creds_from_file()
    if creds[0] == "" or creds[1] == "":
        return True
    else:
        return False


# section of code to run on import of this file. check if creds file exists and has information. if not, notifiy user and end program.
if not check_if_creds_file_exists():
    make_creds_file()
if check_if_creds_file_is_empty():
    show_missing_creds_in_auth_file_gui(
        get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    )
    exit()
