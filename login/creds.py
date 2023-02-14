import PySimpleGUI as sg
import os


# method to get appdata directory
def get_appdata_directory():
    return os.getenv("APPDATA")


# method to make the creds.txt file at appdata/roaming/Py-TwitterBot\creds.txt
def make_creds_file():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    with open(directory, "w") as f:
        f.write('Username: ""' + "\n")
        f.write('Password: ""')
    print(f"Made creds file @ {directory}")


# method to check if creds.txt exists in appdata/roaming/Py-TwitterBot
def check_if_creds_file_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    return os.path.exists(directory)


# method to read the lines in the creds.txt file
def get_creds_from_file():
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


def parse_cred_line(line):
    new_line = ""
    for char in line:
        if char == " " or char == "\n" or char == '"':
            continue
        new_line = new_line + char
    return new_line


def show_missing_creds_in_auth_file_gui(location):
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


def check_if_creds_file_is_empty():
    creds = get_creds_from_file()
    if creds[0] == "" or creds[1] == "":
        return True




if not check_if_creds_file_exists():
    make_creds_file()
if check_if_creds_file_is_empty():
    show_missing_creds_in_auth_file_gui(
        get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    )
    exit()
