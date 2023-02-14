import PySimpleGUI as sg
import sys
import os


# method to get the directory of appdata
def get_appdata_dir():
    """method to get the directory of appdata

    Args:
        None

    Returns:
        string: the directory of appdata

    """

    return os.getenv("APPDATA")


# method to make credentials.txt file in appdata/Py-twitterbot
def make_credentials_file():
    """method to make credentials.txt file in appdata/Py-twitterbot

    Args:
        None

    Returns:
        string: the directory of the twitterbot folder

    """
    dir = get_appdata_dir() + "\Py-twitterbot\credentials.txt"

    # make a file called credentials.txt
    with open(dir, "w") as f:
        f.write('Username: ""\n')
        f.write('Password: ""')
    print(f"Made credentials.txt file at {dir}")


# method to make a directory called Py-TwitterBot in appdata
def make_appdata_dir():
    """method to make a directory called Py-TwitterBot in appdata

    Args:
        None

    Returns:
        None

    """
    # make a directory called Py-twitterbot
    dir = get_appdata_dir() + "\Py-twitterbot"
    os.mkdir(dir)
    print(f"Made Py-TwitterBot directory at {dir}")


# method to check if Py-TwitterBot directory exists in appdata
def check_if_appdata_dir_exists():
    """method to check if Py-TwitterBot directory exists in appdata

    Args:
        None

    Returns:
        boolean: True if the directory exists, False if it does not

    """
    # get the directory of appdata
    appdata_dir = get_appdata_dir()

    # check if the directory exists
    if os.path.exists(appdata_dir + "\Py-twitterbot"):
        return True
    else:
        return False


# method to check if credentials.txt exists in appdata/Py-TwitterBot directory
def check_if_credentials_file_exists():
    """method to check if credentials.txt exists in appdata/Py-TwitterBot directory

    Args:
        None

    Returns:
        boolean: True if the file exists, False if it does not

    """
    # get the directory of appdata
    appdata_dir = get_appdata_dir()

    # check if the file exists
    if os.path.exists(appdata_dir + "\Py-twitterbot\credentials.txt"):
        return True
    else:
        return False


# method to read the credentials.txt file
def get_creds():
    """method to read the credentials.txt file

    Args:
        None

    Returns:
        string,string : username, password from the credentials.txt file

    """
    # get the directory of appdata
    appdata_dir = get_appdata_dir()

    # open the file
    file = open(appdata_dir + "\Py-twitterbot\credentials.txt", "r")

    # read the file
    lines = file.readlines()

    # get the username and password
    username = (lines[0].strip())[11:-1]
    password = (lines[1].strip())[11:-1]

    # return the username and password
    return username, password


# method to check if the creds file has no data in it
def check_if_creds_file_is_empty():
    """method to check if the creds file has no data in it

    Args:
        None

    Returns:
        boolean: True if the file is empty, False if it is not

    """
    creds = get_creds()
    if creds[0] == "" or creds[1] == "":
        return True


# method to show a gui that tells the user to fill out the credentials.txt file
def show_missing_creds_in_auth_file_gui(location):
    """method to show a gui that tells the user to fill out the credentials.txt file

    Args:
        location (string): the location of the credentials.txt file

    Returns:
        None

    """
    THEME = "SystemDefaultForReal"
    out_text = (
        "TWITTER LOGIN CREDENTIALS MISSING IN credentials.txt!\n\n"
        + f"Please write your Twitter login in the file at [{location}] in the format outlined in the new file.\n"
        + "Restart the program after these changes...\n\n"
        + "Credentials are stored only in this location with credentials.py, and are accessed only by the login methods in login.py"
    )
    sg.theme(THEME)
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


# run upon import
# make twitterbot folder if it doesnt exist, make credentials.txt if it doesnt exist, and show a gui if the credentials.txt file is empty
if not check_if_appdata_dir_exists():
    make_appdata_dir()

if not check_if_credentials_file_exists():
    make_credentials_file()

if check_if_creds_file_is_empty():
    print("Please fill out the credentials.txt file in your appdata directory")
    location = get_appdata_dir() + "\Py-twitterbot\credentials.txt"
    show_missing_creds_in_auth_file_gui(location)
    sys.exit()
